import random


def run_monte_carlo_simulation(
    starting_corpus,
    annual_expense,
    years_in_retirement,
    inflation_rate,
    simulations=1000
):

    successful_runs = 0

    ending_values = []

    yearly_records = []

    for sim in range(simulations):

        corpus = starting_corpus

        current_expense = annual_expense

        yearly_path = []

        crash_triggered = False

        for year in range(years_in_retirement):

            #######################################
            # SEQUENCE RISK
            #######################################

            if (
                year < 5
                and not crash_triggered
                and random.random() < 0.30
            ):

                annual_return = random.uniform(
                    -0.30,
                    -0.10
                )

                crash_triggered = True

            else:

                annual_return = (
                    random.normalvariate(
                        0.10,
                        0.15
                    )
                )

            #######################################
            # CORPUS GROWTH
            #######################################

            corpus = corpus * (
                1 + annual_return
            )

            #######################################
            # WITHDRAWAL
            #######################################

            corpus -= current_expense

            #######################################
            # INFLATION
            #######################################

            current_expense = (
                current_expense *
                (
                    1 +
                    inflation_rate / 100
                )
            )

            yearly_path.append(corpus)

            if corpus <= 0:
                break

        if corpus > 0:
            successful_runs += 1

        ending_values.append(corpus)

        yearly_records.append(yearly_path)

    success_rate = (
        successful_runs / simulations
    ) * 100

    return {
        "success_rate": round(
            success_rate,
            1
        ),
        "ending_values": ending_values,
        "yearly_records": yearly_records
    }
