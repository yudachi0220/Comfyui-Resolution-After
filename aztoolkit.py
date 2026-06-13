# ComfyUI - azToolkit - Azornes 2025

import torch
import comfy.model_management

try:
    from .core.auto_detect import (
        apply_backend_auto_detect_fallback,
        calculate_rescale_factor,
        safe_float,
        safe_int,
    )
    from .core.calculation_api import register_calculation_routes
    from .core.dimension_cache import register_dimension_routes, store_detected_dimensions
    from .core.log_system import create_module_logger
except ImportError:
    from core.auto_detect import (
        apply_backend_auto_detect_fallback,
        calculate_rescale_factor,
        safe_float,
        safe_int,
    )
    from core.calculation_api import register_calculation_routes
    from core.dimension_cache import register_dimension_routes, store_detected_dimensions
    from core.log_system import create_module_logger


log = create_module_logger()


class ResolutionMaster:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
        log.debug("Initialized node on device", self.device)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (
                    ["Manual", "Manual Sliders", "Common Resolutions", "Aspect Ratios"],
                    {"tooltip": "选择输出尺寸控制方式。手动(Manual)模式使用分辨率主控画布。"}
                ),
                "latent_type": (
                    ["latent_4x8", "latent_128x16"],
                    {"tooltip": "选择潜空间类型。4x8 适用于 WAN/Anima/Z-Image/Qwen，128x16 适用于 LTX2。"}
                ),
                "width": ("INT", {"default": 512, "min": 0, "max": 32768, "step": 64, "tooltip": "最终输出宽度（像素）。"}),
                "height": ("INT", {"default": 512, "min": 0, "max": 32768, "step": 64, "tooltip": "最终输出高度（像素）。"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 128, "step": 1, "display": "number", "tooltip": "批次大小。使用滑块或直接输入数字控制每批次创建的潜空间数量。"}),
                "auto_detect": ("BOOLEAN", {"default": False, "label_on": "从输入自动检测", "label_off": "手动", "tooltip": "从连接的输入图像自动检测尺寸。"}),
                "auto_detect_source": ("STRING", {"default": "backend", "tooltip": "分辨率主控界面使用的技术设置。"}),
                "auto_detect_width": ("INT", {"default": 0, "min": 0, "max": 32768, "tooltip": "自动检测到的输入宽度。"}),
                "auto_detect_height": ("INT", {"default": 0, "min": 0, "max": 32768, "tooltip": "自动检测到的输入高度。"}),
                "auto_fit_on_change": ("BOOLEAN", {"default": False, "tooltip": "检测到新图像时，自动适配到最接近的预设。"}),
                "auto_resize_on_change": ("BOOLEAN", {"default": False, "tooltip": "检测到新图像时，使用选定的缩放模式自动调整大小。"}),
                "auto_snap_on_change": ("BOOLEAN", {"default": False, "tooltip": "检测到新图像时，按选定的对齐步长取整。"}),
                "smart_fit": ("BOOLEAN", {"default": False, "tooltip": "适配到最接近的预设宽高比，同时保持尺寸接近当前分辨率。"}),
                "use_custom_calc": ("BOOLEAN", {"default": False, "tooltip": "检测到新图像时，自动应用所选模型或类别的尺寸规则。"}),
                "preserve_scaling_ratio": ("BOOLEAN", {"default": False, "tooltip": "缩放时保持图像比例。"}),
                "selected_category": ("STRING", {"default": "", "tooltip": "选中的预设类别。"}),
                "snap_value": ("INT", {"default": 64, "min": 1, "max": 32768, "tooltip": "取整宽高时使用的对齐步长。"}),
                "upscale_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 100.0, "tooltip": "手动缩放倍率。"}),
                "target_resolution": ("INT", {"default": 1080, "min": 1, "max": 32768, "tooltip": "缩放时使用的目标 p-分辨率。"}),
                "target_megapixels": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 1000.0, "tooltip": "缩放时使用的目标百万像素数。"}),
                "auto_detect_presets_json": ("STRING", {"default": "{}", "tooltip": "自动检测使用的技术预设数据。"}),
                "rescale_mode": ("STRING", {"default": "resolution", "tooltip": "重缩放因子输出使用的缩放模式。"}),
                "rescale_value": ("FLOAT", {"default": 1.0, "step": 0.001, "min": 0.0, "max": 100.0, "tooltip": "界面显示的当前重缩放因子值。"}),
            },
            "optional": {
                "input_image": ("IMAGE", {"tooltip": "用于自动检测宽高的可选图像。"}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
            },
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT", "LATENT")
    RETURN_NAMES = ("width", "height", "rescale_factor", "latent")
    OUTPUT_TOOLTIPS = (
        "最终输出宽度（像素）。",
        "最终输出高度（像素）。",
        "根据所选缩放模式计算的缩放因子。",
        "包含所选尺寸、批次大小和潜空间类型的空潜空间。批次大小已合并至其中。",
    )
    DESCRIPTION = "交互式分辨率、缩放、预设和潜空间尺寸助手，支持输入图像自动检测。"
    FUNCTION = "main"
    CATEGORY = "utils/分辨率工具 (azToolkit)"

    @staticmethod
    def detect_image_dimensions(input_image):
        if input_image.dim() == 4:  # [batch, height, width, channels]
            return int(input_image.shape[2]), int(input_image.shape[1])
        if input_image.dim() == 3:  # [height, width, channels]
            return int(input_image.shape[1]), int(input_image.shape[0])
        log.warning("Unsupported input image tensor dimensions", input_image.dim())
        return None

    @staticmethod
    def _is_empty_local_image_gallery_selection(value):
        return str(value or "").strip().lower() in ("", "none", "null", "undefined")

    @classmethod
    def is_empty_local_image_gallery_input(cls, prompt, unique_id):
        if not isinstance(prompt, dict) or unique_id is None:
            return False

        current_node = prompt.get(str(unique_id)) or prompt.get(unique_id)
        input_link = current_node.get("inputs", {}).get("input_image") if isinstance(current_node, dict) else None
        if not isinstance(input_link, (list, tuple)) or not input_link:
            return False

        source_node_id = str(input_link[0])
        source_node = prompt.get(source_node_id) or prompt.get(input_link[0])
        if not isinstance(source_node, dict) or source_node.get("class_type") != "LocalImageGallery":
            return False

        selected_image = source_node.get("inputs", {}).get("selected_image", "")
        return cls._is_empty_local_image_gallery_selection(selected_image)

    def main(
        self,
        mode,
        latent_type,
        width,
        height,
        auto_detect,
        auto_detect_source,
        auto_detect_width,
        auto_detect_height,
        auto_fit_on_change,
        auto_resize_on_change,
        auto_snap_on_change,
        smart_fit,
        use_custom_calc,
        preserve_scaling_ratio,
        selected_category,
        snap_value,
        upscale_value,
        target_resolution,
        target_megapixels,
        auto_detect_presets_json,
        rescale_mode,
        rescale_value,
        batch_size=1,
        input_image=None,
        unique_id=None,
        prompt=None,
    ):
        log.debug(
            "Executing",
            "mode=",
            mode,
            "latent_type=",
            latent_type,
            "width=",
            width,
            "height=",
            height,
            "auto_detect=",
            auto_detect,
        )

        frontend_source_empty = auto_detect_source == "frontend-empty"
        local_image_gallery_empty = self.is_empty_local_image_gallery_input(prompt, unique_id)

        if auto_detect and (frontend_source_empty or local_image_gallery_empty):
            log.debug(
                "Skipping backend auto-detect fallback because frontend source has no active selection",
                "frontend_source_empty=",
                frontend_source_empty,
                "local_image_gallery_empty=",
                local_image_gallery_empty,
            )
        elif auto_detect and input_image is not None:
            detected_dimensions = self.detect_image_dimensions(input_image)
            if detected_dimensions is not None:
                detected_width, detected_height = detected_dimensions
                store_detected_dimensions(unique_id, detected_width, detected_height)
                log.debug(
                    "Detected input dimensions",
                    detected_width,
                    "x",
                    detected_height,
                    "unique_id=",
                    unique_id,
                )

                frontend_matches_tensor = (
                    auto_detect_source == "frontend"
                    and safe_int(auto_detect_width) == detected_width
                    and safe_int(auto_detect_height) == detected_height
                )

                if not frontend_matches_tensor:
                    previous_width, previous_height = width, height
                    width, height = apply_backend_auto_detect_fallback(
                        detected_width,
                        detected_height,
                        auto_fit_on_change,
                        auto_resize_on_change,
                        auto_snap_on_change,
                        smart_fit,
                        use_custom_calc,
                        preserve_scaling_ratio,
                        selected_category,
                        safe_int(snap_value, 64),
                        safe_float(upscale_value, 1.0),
                        safe_int(target_resolution, 1080),
                        safe_float(target_megapixels, 2.0),
                        rescale_mode,
                        auto_detect_presets_json,
                    )
                    log.info(
                        "Applied backend auto-detect fallback",
                        f"{previous_width}x{previous_height}",
                        "->",
                        f"{width}x{height}",
                    )

        rescale_factor = calculate_rescale_factor(
            width,
            height,
            rescale_mode,
            safe_float(upscale_value, 1.0),
            safe_int(target_resolution, 1080),
            safe_float(target_megapixels, 2.0),
        )

        if latent_type == "latent_128x16":
            latent = torch.zeros([batch_size, 128, height // 16, width // 16], device=self.device)
        else:
            latent = torch.zeros([batch_size, 4, height // 8, width // 8], device=self.device)

        log.debug(
            "Returning result",
            "width=",
            width,
            "height=",
            height,
            "rescale_factor=",
            rescale_factor,
            "batch_size=",
            batch_size,
        )
        return (width, height, rescale_factor, {"samples": latent})


register_dimension_routes()
register_calculation_routes()
