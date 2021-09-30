import csv


def send_test_csv_report(test_results):
    filename = "test_csv_report.csv"
    with open(filename, 'w', encoding='UTF-8', newline='') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow([
            'S.No',
            'Test Name',
            'Test Result',
            'Test Description'
        ])
        for result_index, result in enumerate(test_results):
            csv_writer.writerow([
                result_index + 1,
                result['test_name'],
                result['result'],
                result['test_description']
            ])