settings = {
    "comparison_columns": [
        {
            "num_levels": 3,
            "term_frequency_adjustments": True,
            "col_name": "first_name"
        },
        {
            "num_levels": 3,
            "term_frequency_adjustments": True,
            "col_name": "surname"
        },
        {
            "col_name": "dob"
        },
        {
            "col_name": "city"
        },
        {
            "col_name": "email"
        }
    ],
    "blocking_rules": [
        "l.first_name = r.first_name",
        "l.surname = r.surname"
    ],
    "link_type": "dedupe_only",

}