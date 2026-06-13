// 分辨率主控工具提示配置
// 包含分辨率主控和预设管理器的提示文本

export const tooltips = {
    // 主控制（不含滑块和2D画布）
    swapBtn: "交换宽度和高度。",
    snapBtn: "按选定的对齐步长取整当前尺寸。",
    snapValueArea: "点击输入自定义对齐步长。",
    
    // 输出值区域（可编辑）
    widthValueArea: "点击手动输入宽度。",
    heightValueArea: "点击手动输入高度。",
    batchSizeValueArea: "滑动或点击输入每批次创建的图像数量。",
    latValueArea: "选择潜空间类型。大多数模型使用 4x8，Flux.2 使用 128x16。",
    
    // 缩放控制（仅按钮和下拉框）
    scaleBtn: "按选定的倍率缩放当前尺寸。",
    upscaleRadio: "使用此倍率作为重缩放因子输出。",
    scaleValueArea: "点击输入缩放倍率，例如 2 或 /2。",
    
    resolutionBtn: "缩放当前尺寸以匹配选定的 p-分辨率。",
    resolutionDropdown: "选择目标 p-分辨率。",
    resolutionRadio: "使用选定的 p-分辨率作为重缩放因子输出。",
    resolutionValueArea: "点击输入缩放值。分辨率主控将将其转换为 p-分辨率。",
    
    megapixelsBtn: "缩放当前尺寸至选定的百万像素目标。",
    megapixelsRadio: "使用百万像素目标作为重缩放因子输出。",
    megapixelsValueArea: "点击输入目标百万像素数。",
    preserveScalingRatioCheckbox: "调整大小时保持精确的宽高比。也会影响智能适配。",
    
    // 自动检测控制
    autoDetectToggle: "从连接的输入图像检测尺寸。",
    autoFitBtn: "立即将当前尺寸适配到最接近的预设。",
    autoFitCheckbox: "检测到新图像时，自动适配到最接近的预设。",
    smartFitToggle: "适配到最接近的预设宽高比，同时保持尺寸接近当前分辨率。",
    autoResizeBtn: "立即使用选定的缩放模式调整当前尺寸。",
    autoResizeCheckbox: "检测到新图像时，使用选定的缩放模式自动调整大小。",
    autoSnapBtn: "立即按选定的对齐步长取整当前尺寸。",
    autoSnapCheckbox: "检测到新图像时，按选定的对齐步长取整尺寸。",
    detectedInfo: "点击直接使用检测到的图像尺寸。",
    autoDetectLiveStatus: "显示尺寸是否立即更新或仅在运行工作流后更新。",
    
    // 预设控制
    categoryDropdown: "选择预设分类。",
    presetDropdown: "选择分辨率预设。",
    managePresetsBtn: "打开预设管理器进行添加、编辑、隐藏或删除预设。",
    customCalcCheckbox: "检测到新图像时，自动应用所选模型或类别的尺寸规则。",
    autoCalcBtn: "立即应用所选模型或类别的尺寸规则。",
    calcInfoToggle: "显示或隐藏所选计算规则的信息。",
    compactToggleBtn: "显示或隐藏 2D 画布下方的额外区域。",
    compactHelpBtn: "打开快捷键和项目链接。",
    
    // 区域标题
    extraControlsHeader: "显示或隐藏额外区域。",
    actionsHeader: "显示或隐藏操作区域。",
    scalingHeader: "显示或隐藏缩放区域。",
    autoDetectHeader: "显示或隐藏自动检测区域。",
    presetsHeader: "显示或隐藏预设区域。"
};

// 预设管理器对话框工具提示
export const presetManagerTooltips = {
    // 底部按钮
    'add-preset-btn': '添加自定义分辨率预设。',
    'delete-selected-btn': '删除选中的自定义预设。使用 Shift+点击以选择范围。',
    'import-btn': '从 JSON 文件导入预设并与当前预设合并。',
    'export-btn': '将自定义预设和隐藏的内置预设导出为 JSON 文件。',
    'edit-json-btn': '以 JSON 格式编辑完整的预设配置。',
    'close-btn': '关闭预设管理器对话框。',
    'back-btn': '返回预设列表。',
    
    // 添加/编辑视图
    'category-select-btn': '选择已有分类或输入新分类名称。',
    'resolution-master-preset-add-rename-category-btn': '重命名选中的分类。',
    'quick-add-button': '添加此预设或保存当前预设更改。',
    
    // 列表视图
    'manage-presets-btn': '打开预设管理器进行添加、编辑、隐藏或删除预设。',
    'resolution-master-preset-list-edit-btn': '编辑此预设。',
    'resolution-master-preset-list-delete-btn': '删除此自定义预设。',
    'resolution-master-preset-toggle-btn': '切换此内置预设的可见性。',
    'resolution-master-preset-list-edit-category-btn': '打开此分类以添加或编辑预设。',
    'resolution-master-preset-list-category-header': '拖拽以重新排序分类。',
    'resolution-master-preset-list-category-name': '双击重命名此分类。',
    'resolution-master-preset-list-name': '双击重命名此预设。',
    'resolution-master-preset-list-checkbox': '选中此预设以进行批量删除。',
    'resolution-master-preset-list-clone-handle': '拖拽以复制此预设。',
    'resolution-master-aspect-ratio-preset-action-btn': {
        'delete': '删除此自定义预设。',
        'hide': '在主预设列表中隐藏此内置预设。',
        'unhide': '在主预设列表中重新显示此内置预设。'
    },
    
    // JSON 编辑器对话框
    'json-editor-close-btn': '关闭 JSON 编辑器（不保存）。',
    'json-editor-format-btn': '自动格式化 JSON 并正确缩进（Ctrl+Shift+F）。',
    'json-editor-cancel-btn': '放弃更改并关闭编辑器。',
    'json-editor-apply-btn': '应用此 JSON 并替换当前预设配置。'
};
