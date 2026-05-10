#################################################
# BUCKET STRATEGY ENGINE
#################################################

def generate_bucket_strategy(

    retirement_corpus,

    required_corpus,

    survivability,

    current_age,

    retirement_age,

    inflation_rate
):

    #################################################
    # CORPUS COVERAGE RATIO
    #################################################

    corpus_ratio = (

        retirement_corpus /

        required_corpus
    )

    #################################################
    # SAFE WITHDRAWAL RATE
    #################################################

    swr = 0.03

    if (

        survivability >= 90

        and

        corpus_ratio >= 1.75
    ):

        swr = 0.04

    elif (

        survivability >= 80

        and

        corpus_ratio >= 1.4
    ):

        swr = 0.035

    #################################################
    # SAFE YEARLY WITHDRAWAL
    #################################################

    yearly_withdrawal = (

        retirement_corpus * swr
    )

    #################################################
    # MONTHLY WITHDRAWAL
    #################################################

    monthly_withdrawal = (

        yearly_withdrawal / 12
    )

    #################################################
    # BUCKET 1
    # 5 YEARS
    #################################################

    bucket_1 = (

        yearly_withdrawal * 5
    )

    #################################################
    # BUCKET 2
    # NEXT 7 YEARS
    #################################################

    bucket_2 = (

        yearly_withdrawal * 7
    )

    #################################################
    # BUCKET 3
    #################################################

    bucket_3 = (

        retirement_corpus

        -

        bucket_1

        -

        bucket_2
    )

    #################################################
    # RATIOS
    #################################################

    bucket_1_ratio = (

        bucket_1 /

        retirement_corpus
    ) * 100

    bucket_2_ratio = (

        bucket_2 /

        retirement_corpus
    ) * 100

    bucket_3_ratio = (

        bucket_3 /

        retirement_corpus
    ) * 100

    #################################################
    # REFILL STRATEGY
    #################################################

    refill_strategy = [

        "Refill Safety Bucket every 2 years.",

        "Refill Bucket 1 from Bucket 2 during stable market periods.",

        "Refill Bucket 2 from Bucket 3 during strong equity years.",

        "Avoid equity withdrawals during major market drawdowns."
    ]

    #################################################
    # RETURN
    #################################################

    return {

        "swr": swr * 100,

        "monthly_withdrawal": monthly_withdrawal,

        "yearly_withdrawal": yearly_withdrawal,

        "bucket_1": bucket_1,

        "bucket_2": bucket_2,

        "bucket_3": bucket_3,

        "bucket_1_ratio": bucket_1_ratio,

        "bucket_2_ratio": bucket_2_ratio,

        "bucket_3_ratio": bucket_3_ratio,

        "corpus_ratio": corpus_ratio,

        "refill_strategy": refill_strategy
    }
