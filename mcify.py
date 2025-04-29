import argparse
from tran import model_to_minecraft, START_POS, ROTATE_ANGLE, PITCH, GAME_VERSION
# example: python mcify.py model.obj world_path --start-pos 10,20,30 --rotate 45,0,0 --pitch 0.5 --version 1.20.1 --no-wool --no-glass

def parse_tuple(tuple_str):
    try:
        x, y, z = map(float, tuple_str.split(','))
        return (x, y, z)
    except:
        raise argparse.ArgumentTypeError("--start-pos and --rotate must be in the format x,y,z")

def parse_version(ver_str):
    try:
        major, minor, patch = map(int, ver_str.split('.'))
        return ("java", (major, minor, patch))
    except:
        raise argparse.ArgumentTypeError("--version must be in the format major.minor.patch")

def main():
    parser = argparse.ArgumentParser(description='将3D模型转换为Minecraft方块')
    
    # 必需参数
    parser.add_argument('obj_file', help='Model file path | 模型文件路径')
    parser.add_argument('world_path', help='Minecraft world path | Minecraft 世界路径')
    
    # 可选参数
    parser.add_argument('--start-pos', type=parse_tuple, default=START_POS,
                       help='start position x,y,z | 起始位置 x,y,z')
    parser.add_argument('--rotate', type=parse_tuple, default=ROTATE_ANGLE,
                       help='rotate angle rx,ry,rz | 旋转角度 rx,ry,rz')
    parser.add_argument('--pitch', type=float, default=PITCH,
                       help='voxel pitch | 体素大小')
    parser.add_argument('--version', type=parse_version, default=GAME_VERSION,
                       help='Minecraft version | Minecraft 版本')
    
    # 方块类型选项
    parser.add_argument('--no-wool', action='store_false', dest='wool',
                       help='don\'t use wool blocks | 不使用羊毛方块')
    parser.add_argument('--no-concrete', action='store_false', dest='concrete',
                       help='don\'t use concrete blocks | 不使用混凝土方块')
    parser.add_argument('--no-terracotta', action='store_false', dest='terracotta',
                       help='don\'t use terracotta blocks | 不使用陶瓦方块')
    parser.add_argument('--no-glass', action='store_false', dest='glass',
                       help='don\'t use glass blocks | 不使用玻璃方块')
    
    args = parser.parse_args()
    
    model_to_minecraft(
        obj_file=args.obj_file,
        world_path=args.world_path,
        start_pos=args.start_pos,
        rotate_angle=args.rotate,
        pitch=args.pitch,
        game_version=args.version,
        wool=args.wool,
        concrete=args.concrete,
        terracotta=args.terracotta,
        glass=args.glass
    )

if __name__ == '__main__':
    main()