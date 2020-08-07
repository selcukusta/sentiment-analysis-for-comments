
import csv
import argparse
import enum
import sys
from normalizer import normalizer
from common import common


def RepresentsFloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    ft_type = enum.Enum("ft_type", ("train", "valid"))
    parser = argparse.ArgumentParser(
        description='Hazır veri setinde yer alan yorumları FastText kütüphanesi kullanımı için etiketleyerek kaydeder.')
    parser.add_argument('--ft_type', type=str, nargs='?',
                        choices=tuple(t.name for t in ft_type),
                        default=ft_type.train.name,
                        help='FastText öğrenmesi esnasında kullanım tipini giriniz')
    parser.add_argument('--start_line', type=int, nargs='?', const=2,
                        default=2,
                        help='Okumaya başlanacak satır sayısını giriniz')

    args = parser.parse_args()
    inputs = []
    with open(f"dataset/sentiment_data.csv", 'r') as f:
        reader = csv.reader(f)
        [next(reader, None) for item in range(args.start_line - 1)]
        for row in reader:
            rate_is_convertable = RepresentsFloat(row[1])
            if rate_is_convertable:
                label = "__label__"
                comment = normalizer.normalize(row[2])
                rate = float(row[1])
                if rate == 0:
                    label += "negative"
                elif rate == 1:
                    label += "positive"
                else:
                    label += "notr"
                inputs.append(f"{label} {comment}")

        common.colored_print(
            common.bcolors.WARNING, f"All items {len(inputs)} are labeled. {args.ft_type} file creation is starting...")

    with open(f'dataset/comments.{args.ft_type}', 'a') as f:
        for item in inputs:
            f.write(f"{item}\n")

    common.colored_print(common.bcolors.OKBLUE, "=== COMPLETED ===")
