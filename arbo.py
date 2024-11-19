import random
import argparse

def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser(
        prog="arbo",
        description="Simple probabilistic ASCII-art tree generator"
    )

    # Add arguments
    parser.add_argument("width", type=int, help="Width of the tree grid")
    parser.add_argument("height", type=int, help="Height of the tree grid")
    parser.add_argument("start", type=int, help="Starting position indexed from 1, or 0 for random")
    parser.add_argument("spread", type=int, help="Total width a branch can spread, centered on branch")
    parser.add_argument("gen", type=int, nargs="+", help="Probabilities as percentages for each spread position (one value per spread range) followed by reduction factors as percentages (e.g., gen1 gen2 ... genSpread reduce1 reduce2 ... reduceSpread)")

    # Parse arguments
    args = parser.parse_args()

    # Validate command line arguments
    expected_length = args.spread * 2
    if len(args.gen) != expected_length:
        parser.error(f"Expected {expected_length} integers for 'gen' and 'reduce', but got {len(args.gen)}.")
    if args.width < 1:
        parser.error(f"'width' must be at least 1. Got {args.width}.")
    if args.height < 1:
        parser.error(f"'height' must be at least 1. Got {args.height}.")
    if not (0 <= args.start <= args.width):
        parser.error(f"'start' must be 0 or from 1 to 'width' = {args.width} inclusive. Got {args.start}.")
    
    return args

def main():
    # Parse arguments
    args = parse_arguments()

    # Initialize variables
    width = args.width
    height = args.height
    start = args.start
    spread = args.spread

    if start == 0:
        start = random.randint(1, width)

    # Split 'gen' into probabilities and reduction factors
    gen = args.gen[:spread]
    reduce = args.gen[spread:]

    # Initialize tree
    tree = [[' ' for _ in range(width)] for _ in range(height)]
    tree[0][start-1] = "|"

    # Generate the tree
    for y in range(1, height):
        for x in range(width):
            if tree[y - 1][x] not in [' ', 'o']:
                for s in range(spread):
                    target = s + x - spread // 2
                    if 0 <= target < width and random.randint(1, 100) <= gen[s]:
                        if tree[y][target] != ' ':
                            tree[y][target] = 'o'
                        else:
                            tree[y][target] = (
                                '|' if s - spread // 2 == 0 else
                                '\\' if s == 0 else
                                '/' if s == spread - 1 else
                                '_'
                            )
        # Update generation probabilities
        gen = [int(g * r / 100) for g, r in zip(gen, reduce)]

    # Print the tree with borders
    border = "═" * width
    print("\n\t╔" + border + "╗")
    for row in reversed(tree):
        print("\t║" + "".join(row) + "║")
    print("\t╚" + border + "╝")

if __name__ == "__main__":
    main()
