import pandas as pd


def complex_distance(a, b):
    return a - b


def main():
    names = ["rus", "en_r1", "en_r123", "dutch"]
    limits = [0.07, 0.08, 0.09, 0.1, 0.15, 0.2]

    for name in names:
        for limit in limits:
            input_file = f"eigvals_with_limits/{name}/{limit}.csv"
            output_file = f"eigvals_with_limits/{name}/z_{limit}.csv"

            data = pd.read_csv(input_file, header=None)

            if data.empty:
                raise ValueError("CSV файл пуст или данные не были прочитаны.")

            data[0] = data[0].apply(lambda x: complex(x.replace("(", "").replace(")", "")))

            eigenvalues = data[0].values
            z_statistics = []

            for i in range(len(eigenvalues)):
                distances = [
                    complex_distance(eigenvalues[i], eigenvalues[j])
                    for j in range(len(eigenvalues))
                    if i != j
                ]

                closest_distance = min(distances, key=abs)
                second_closest_distance = sorted(distances, key=abs)[1]

                z_statistics.append(closest_distance / second_closest_distance)

            z_statistics_df = pd.DataFrame({"z_statistic": z_statistics})
            z_statistics_df.to_csv(output_file, index=False)
            print(f"Z-статистика записана в файл {output_file}")


if __name__ == "__main__":
    main()
