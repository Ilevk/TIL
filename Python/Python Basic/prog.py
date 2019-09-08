# Argument Parser, Python docs : https://docs.python.org/3.6/library/argparse.html
# 16.4.1 Example
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
# Parser 설명 추가해주면, help 명령어를 사용했을 때, 설명이 나온다.
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
# argment 추가하는건데, 정수형 인자들을 인식한다, type에 int를 줘서 지명할 수 있는듯, 
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))