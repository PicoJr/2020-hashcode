import argparse
import heapq
import tqdm
from typing import List, Callable, Tuple
from score import compute_score

from parser import InputDataSet, Library, parse_input_file, LibraryOrder, OutputDataSet, write_output_file


def nbest_books(n, books, book_score: Callable[[int], int]) -> List[int]:
    return heapq.nlargest(n, books, key=book_score)


def max_books_sent(library: Library, days_left: int) -> int:
    return (days_left - library.signup_delay) * library.books_per_day


def library_best_books(library: Library, days_left: int, book_score: Callable[[int], int]) -> List[int]:
    max_books_sent_n = max_books_sent(library, days_left)
    if max_books_sent_n <= 0:
        return []
    return nbest_books(max_books_sent_n, library.books, book_score)


def solve(input_data: InputDataSet) -> OutputDataSet:
    libraries_not_selected = input_data.libraries.copy()
    updated_book_score = input_data.book_scores.copy()
    days_left = input_data.n_days

    def book_score(b: int) -> int:
        return updated_book_score[b]

    def max_library_key(ilib) -> int:
        _i, lib = ilib
        return sum(book_score(b) for b in library_best_books(lib, days_left, book_score)) / lib.signup_delay

    def best_library(libraries: List[Library]) -> Tuple[int, Library]:
        return max(enumerate(libraries), key=max_library_key)

    library_orders = []
    pbar = tqdm.tqdm(total=len(libraries_not_selected))
    while len(libraries_not_selected) > 0:
        i_best, best = best_library(libraries_not_selected)
        pbar.update(1)
        libraries_not_selected.pop(i_best)
        days_left -= best.signup_delay
        best_books = library_best_books(best, days_left, book_score)
        library_score = sum(book_score(b) for b in best_books)
        if library_score <= 0:
            break
        for book in best_books:
            updated_book_score[book] = 0
        library_orders.append(LibraryOrder(best.id_, len(best_books), best_books))
    pbar.close()
    return OutputDataSet(len(library_orders), library_orders)


def main():
    parser = argparse.ArgumentParser(description="hashcode-2020 solver")
    parser.add_argument("input", nargs='+', help="input file")
    parser.add_argument("--output", "-o", default="tmp.out", help="output file (ignored if multiple input file)")
    args = parser.parse_args()
    total_score = 0
    multiple = len(args.input) > 1
    for input_file_path in args.input:
        print(input_file_path)
        with open(input_file_path) as input_file:
            input_data_set = parse_input_file(input_file)
        output_data = solve(input_data_set)
        score = compute_score(input_data_set, output_data)
        total_score += score
        print(f"score: {score:,}")
        output_file_path = f"{input_file_path}.out" if multiple else args.output
        with open(output_file_path, "w+") as output_file:
            write_output_file(output_data, output_file)
    if multiple:
        print(f"total score: {total_score:,}")


if __name__ == "__main__":
    main()
