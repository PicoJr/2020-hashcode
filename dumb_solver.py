import argparse
import io
from typing import List
from score import compute_score

from parser import InputDataSet, Library, parse_input_file, LibraryOrder, OutputDataSet, write_output_file


def average_book(library: Library, book_scores: List[int]) -> float:
    assert library.n_books > 0
    return sum(book_scores[book_id] for book_id in library.books) / library.n_books


def library_heuristic(library: Library, days, book_scores: List[int]) -> float:
    assert days - library.signup_delay != 0
    return library.books_per_day / (days - library.signup_delay) * average_book(library, book_scores)


def solve(input_data: InputDataSet) -> OutputDataSet:
    def sort_key(lib: Library):
        return library_heuristic(lib, input_data.n_days, input_data.book_scores)

    libraries_sorted_by_heuristic = sorted(input_data.libraries, key=sort_key)
    n_libraries = len(libraries_sorted_by_heuristic)
    library_orders = []
    for library in libraries_sorted_by_heuristic:
        library_orders.append(LibraryOrder(library.id_, len(library.books), list(library.books)))
    return OutputDataSet(n_libraries, library_orders)


def main():
    parser = argparse.ArgumentParser(description="hashcode-2020 solver")
    parser.add_argument("input", help="input file")
    parser.add_argument("--output", "-o", default="tmp.out", help="input file")
    args = parser.parse_args()
    with open(args.input) as input_file:
        input_data_set = parse_input_file(input_file)
        print(input_data_set)
    output_data = solve(input_data_set)
    score = compute_score(input_data_set, output_data)
    print(f"score: {score}")
    with open(args.output, "w+") as output_file:
        write_output_file(output_data, output_file)


if __name__ == "__main__":
    main()
