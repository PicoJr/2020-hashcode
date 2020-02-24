import argparse

from parser import InputDataSet, OutputDataSet, parse_input_file, parse_output_file, build_signup_schedule


def compute_score(input_data_set: InputDataSet, output_data_set: OutputDataSet):
    score = 0
    books_already_sent = {}
    signup_schedule = build_signup_schedule(input_data_set.libraries)
    signed_up = []
    not_signed_up_yet = [library.id_ for library in output_data_set.library_orders]
    for day in signup_schedule:
        signup_finished_id = not_signed_up_yet.pop()
        signed_up.append(signup_finished_id)
        print(f"day {day}: library {signup_finished_id} signup is finished")
        days_left = input_data_set.n_days - day
        n_books_sent = days_left * input_data_set.libraries[signup_finished_id].books_per_day
        n_books_sent = min(n_books_sent, output_data_set.library_orders[signup_finished_id].n_books)
        books_sent = output_data_set.library_orders[signup_finished_id].books[:n_books_sent]
        print(f"day {day}: books sent {books_sent}")
        library_score = 0
        for book in books_sent:
            if book not in books_already_sent:
                book_score = input_data_set.book_scores[book]
                library_score += book_score
        score += library_score
    return score


def main():
    parser = argparse.ArgumentParser(description="hashcode-2020 solver")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    args = parser.parse_args()
    with open(args.input) as input_file:
        input_data_set = parse_input_file(input_file)
        print(input_data_set)
    with open(args.output) as output_file:
        output_data_set = parse_output_file(output_file)
        print(output_data_set)

    score = compute_score(input_data_set, output_data_set)
    print(score)


if __name__ == "__main__":
    main()
