# model-transform

此工具用来转换yolo模型，并同时提供下载

如果单独下载 / 转换模型建议直接使用yolo命令行而不是transform.py，此工具意在一次转换 / 下载多个

## 安装

目前依然没有找到arm64上Linux转换的方法，只支持x86_64 Linux 和 macOS（x86_64 & arm）

`poetry install`

## 使用

激活虚拟环境

`poetry shell`

强烈建议认真看完help信息

使用范例：

`python transform.py transform yolo11n.pt -e format=coreml -e imgsz=640`

`python transform.py download yolo11s.pt -o <path-to-save>`

-e/--export-param 可以传递yolo export参数，参数如下

| 参数名      | 类型           | 默认值                     | 描述                                                                 |
|-------------|----------------|---------------------------|----------------------------------------------------------------------|
| format      | str            | 无                        | 导出模型的格式，例如 'onnx', 'torchscript', 'coreml'。               |
| half        | bool           | 无                        | 是否将模型导出为半精度（FP16）。                                     |
| int8        | bool           | 无                        | 是否将模型导出为 INT8 精度（量化）。                                 |
| device      | str \| None    | None                     | 指定运行导出过程的设备，例如 'cpu' 或 'cuda:0'。                     |
| workspace   | int            | 无                        | TensorRT 引擎的最大内存工作空间大小（以 MB 为单位）。                |
| nms         | bool           | 无                        | 是否在模型中添加非极大值抑制（NMS）模块。                            |
| simplify    | bool           | 无                        | 是否简化 ONNX 模型图（减少冗余）。                                   |
| dynamic     | bool           | 无                        | 是否支持动态输入尺寸（例如 ONNX 和 TensorRT 支持的动态形状）。        |
| imgsz       | int \| tuple   | self.model.args['imgsz'] | 输入图像的大小，可以是单个整数（正方形）或元组 (height, width)。     |
| batch       | int            | 1                         | 导出模型时的批处理大小。                                             |
| data        | str \| None    | None                     | 数据集的配置文件路径（用于某些导出格式）。                           |
| verbose     | bool           | False                    | 是否启用详细的日志输出。                                             |
| overrides   | dict           | 无                        | 提供覆盖默认参数的字典。                                             |
| mode        | str            | 'export'                 | 当前操作模式，固定为 'export'。                                      |

完整help信息如下

```bash
Usage: transform.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download
  transform

子命令帮助:

download:
Usage: transform.py [OPTIONS] [MODEL]...

  Options:
    -o, --output TEXT  Output model file
    --help             Show this message and exit.
transform:

  export-param可以传递export模型的参数，支持参数如下

  动态参数表:
  参数名            类型             默认值                 描述
  ============================================================================
  ====
  format         str            无                   导出模型的格式，例如 'onnx',
  'torchscript', 'coreml'。
  half           bool           无                   是否将模型导出为半精度（FP16）。
  int8           bool           无                   是否将模型导出为 INT8 精度（量化）。
  device         str | None     None                指定运行导出过程的设备，例如 'cpu' 或
  'cuda:0'。
  workspace      int            无                   TensorRT 引擎的最大内存工作空间大小（以
  MB 为单位）。
  nms            bool           无                   是否在模型中添加非极大值抑制（NMS）模块。
  simplify       bool           无                   是否简化 ONNX 模型图（减少冗余）。
  dynamic        bool           无                   是否支持动态输入尺寸（例如 ONNX 和
  TensorRT 支持的动态形状）。
  imgsz          int | tuple
  self.model.args['imgsz']输入图像的大小，可以是单个整数（正方形）或元组 (height, width)。
  batch          int            1                   导出模型时的批处理大小。
  data           str | None     None                数据集的配置文件路径（用于某些导出格式）。
  verbose        bool           False               是否启用详细的日志输出。
  overrides      dict           无                   提供覆盖默认参数的字典。
  mode           str            'export'            当前操作模式，固定为 'export'。
Usage: transform.py [OPTIONS] [MODEL]...

  Options:
    -o, --output TEXT        Output model file
    -e, --export-param TEXT  Dynamic export parameters in key=value format,
                             e.g., --e format=onnx.
    --help                   Show this message and exit.
```


## TODO

- 编译arm64 libcoremlpython, libmilstoragepython