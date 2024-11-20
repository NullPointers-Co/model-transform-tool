import shutil
import os

import click


# 参数表
PARAMETERS = [
    ["format", "str", "无", "导出模型的格式，例如 'onnx', 'torchscript', 'coreml'。"],
    ["half", "bool", "无", "是否将模型导出为半精度（FP16）。"],
    ["int8", "bool", "无", "是否将模型导出为 INT8 精度（量化）。"],
    ["device", "str | None", "None", "指定运行导出过程的设备，例如 'cpu' 或 'cuda:0'。"],
    ["workspace", "int", "无", "TensorRT 引擎的最大内存工作空间大小（以 MB 为单位）。"],
    ["nms", "bool", "无", "是否在模型中添加非极大值抑制（NMS）模块。"],
    ["simplify", "bool", "无", "是否简化 ONNX 模型图（减少冗余）。"],
    ["dynamic", "bool", "无", "是否支持动态输入尺寸（例如 ONNX 和 TensorRT 支持的动态形状）。"],
    ["imgsz", "int | tuple", "self.model.args['imgsz']", "输入图像的大小，可以是单个整数（正方形）或元组 (height, width)。"],
    ["batch", "int", "1", "导出模型时的批处理大小。"],
    ["data", "str | None", "None", "数据集的配置文件路径（用于某些导出格式）。"],
    ["verbose", "bool", "False", "是否启用详细的日志输出。"],
    ["overrides", "dict", "无", "提供覆盖默认参数的字典。"],
    ["mode", "str", "'export'", "当前操作模式，固定为 'export'。"]
]

class CustomCommand(click.Group):
    def format_help(self, ctx, formatter):
        super().format_help(ctx, formatter)

        def print_parameters_help():
            formatter.write_text("\n")
            formatter.write_text("\nexport-param可以传递export模型的参数，支持参数如下\n")
            formatter.write_text("\n")
            formatter.write_text("\n动态参数表:\n")
            formatter.write_text(f"{'参数名':<15}{'类型':<15}{'默认值':<20}{'描述'}")
            formatter.write_text("=" * 80)
            for param in PARAMETERS:
                formatter.write_text(f"{param[0]:<15}{param[1]:<15}{param[2]:<20}{param[3]}")

        formatter.write_text("\n")
        formatter.write_text("\n子命令帮助:\n")
        formatter.write_text("\n")
        for command in self.list_commands(ctx):
            cmd = self.get_command(ctx, command)
            formatter.write_text(f"\n{command}:\n")
            with formatter.indentation():
                if command == 'transform':
                    print_parameters_help()
                cmd.format_help(ctx, formatter)


def convert_value(value):
    if value.lower() in ['true', 'false']:  
        return value.lower() == 'true'
    try:
        return int(value)  
    except ValueError:
        try:
            return float(value)  
        except ValueError:
            return value

def _transform(yolo_model, **kwargs):
    from ultralytics import YOLO
    yolo_model = YOLO(yolo_model)
    _outfile_path = yolo_model.export(**kwargs)
    return _outfile_path

def _download(model_name, outpath):
    from ultralytics import YOLO
    yolo_model = YOLO(model_name)
    if outpath:
        _file = os.path.join(outpath, model_name)
        yolo_model.save(_file)
        click.echo(f"Model saved to {_file}")
    else:
        yolo_model.save()
        click.echo(f"Model saved")

@click.group(cls=CustomCommand)
def cli():
    pass

@cli.command()
@click.argument('model', nargs=-1)
@click.option('-o', '--output', type=str, help='Output model file')
@click.option('-e', '--export-param', multiple=True, nargs=1,
              help='Dynamic export parameters in key=value format, e.g., --e format=onnx.')
def transform(model, output, export_param):
    export_kwargs = {}
    for param in export_param:
        if '=' in param:
            key, value = param.split('=', 1)
            export_kwargs[key] = convert_value(value)
        else:
            raise click.BadParameter(f"Invalid format for export parameter: {param}. Expected key=value.")

    for yolo_model in model:
        if os.path.exists(yolo_model):
            click.echo(f"Transforming {yolo_model}...")
        else:
            click.echo(f"File {yolo_model} not found. Using online model instead.")

        outfile_path = _transform(yolo_model, **export_kwargs)

        if output:
            shutil.move(outfile_path, output)
            click.echo(f"Model saved to {output}")
        else:
            click.echo(f"Model saved to {outfile_path}")

@cli.command()
@click.argument('model', nargs=-1)
@click.option('-o', '--output', type=str, help='Output model file')
def download(model, output):
    for model_name in model:
        click.echo(f"Downloading {model_name}...")
        _download(model_name, output)

if __name__ == "__main__":
    head_text = """
░▒▓███████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░       ░▒▓██████▓▒░  

Copyright (c) 2024 by NullPinters Co
"""

    click.echo(head_text)
    cli()
