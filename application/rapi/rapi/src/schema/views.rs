table! {
    use diesel::sql_types::*;
    use note_categories::models::NoteCategorySql;
    notes_cache (id) {
        id -> Int8,
        nickname -> Varchar,
        lastname -> Varchar,
        firstname -> Varchar,
        mail -> Varchar,
        tel -> Varchar,
        birthdate -> Int4,
        promo -> Varchar,
        photo_path -> Nullable<Varchar>,
        note -> Numeric,
        overdraft_date -> Nullable<Date>,
        ecocups -> Int4,
        last_agio -> Nullable<Date>,
        mails_inscription -> Bool,
        stats_inscription -> Bool,
        agios_inscription -> Bool,
        tot_cons -> Numeric,
        tot_refill -> Numeric,
        categories -> Array<NoteCategorySql>,
        hidden -> Bool,
    }
}
