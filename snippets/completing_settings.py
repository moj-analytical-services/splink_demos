from splink.settings import complete_settings_dict

settings = {
    "link_type": "dedupe_only",
    "comparison_columns": [
        {
            "col_name": "first_name"
        }
    ]   
}
completed_settings(settings)