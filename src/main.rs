use chrono::{Datelike, Utc};
use clap::Parser;
use polars::prelude::*;
use std::fs::File;

#[derive(Parser, Debug)]
struct Cli {
    #[arg(long)]
    ticker: String,

    #[arg(long)]
    limit: i16,
}

fn calculate(data: &mut DataFrame, days: i16, limit: i16) {
    let mut volatility_measurements: Vec<f64> = Vec::new();
    let mut _comparison_price: f64;
    let mut _current_row: i32 = 0;

    let random_data: Vec<i32> = (1..=3170).collect();
    let c = Series::new("percent_change", random_data);
    data.with_column(c).unwrap();
    // println!("{data}");

    let start_index = if limit == 0 {
        1
    } else {
        data.height() - limit as usize
    };

    let comparisonData = data.clone();

    let off_by_one_df: PolarsResult<DataFrame> = df!("date" => &["0000-01-01"],
                                      "adjclose" => &[0.0]);

    let res: Series = data
        .column("adjclose")
        .unwrap()
        .f64()
        .expect("Series was not an f64 dtype")
        .into_iter()
        .map(|x| 1.1)
        .collect::<Series>();

    println!("{}", res);
    //
    // volatility_measurements.push(0.0);
    // for row in start_index..data.height() {
    //     let target_day = data.get_row(row).unwrap();
    //     let comparison_day = data.get_row(row - 1_usize).unwrap();
    //     let a = target_day["a"];
    //
    //     let diff: f64 = 1.1;
    //
    //     let percent_change: f64 = 1.1;
    //
    //     volatility_measurements.push(percent_change);
    //
    //     //         if (currentRow >= days):
    //     //             comparisonPrice = dataRange.iloc[currentRow - days]["adjclose"]
    //     //
    //     //         currentDaysPrice = row["adjclose"]
    //     //         date = row["Unnamed: 0"]
    //     //
    //     //         if (comparisonPrice != None):
    //     //             diff = currentDaysPrice - comparisonPrice
    //     //             percentChange = round((diff / comparisonPrice) * 100, 2)
    //     //             volatilityMeasurements.append(
    //     //                 { "date": date, "percent_change": percentChange }
    //     //             )
    //
    //     println!("{volatility_measurements:?}");
    // }
}
// def calculate(data, days, limit = None):
//     volatilityMeasurements = []
//     comparisonPrice = None
//     currentRow = 0
//
//     dataRange = data[-limit:] if limit else data
//
//     for _, row in dataRange.iterrows():
//         if (currentRow >= days):
//             comparisonPrice = dataRange.iloc[currentRow - days]["adjclose"]
//
//         currentDaysPrice = row["adjclose"]
//         date = row["Unnamed: 0"]
//
//         if (comparisonPrice != None):
//             diff = currentDaysPrice - comparisonPrice
//             percentChange = round((diff / comparisonPrice) * 100, 2)
//             volatilityMeasurements.append(
//                 { "date": date, "percent_change": percentChange }
//             )
//
//         currentRow += 1
//
//     return pd.DataFrame(volatilityMeasurements)

fn main() {
    let args = Cli::parse();

    let now = Utc::now();
    let date = format!("{:04}-{:02}-{:02}", now.year(), now.month(), now.day());

    let csv_path: String = format!("./data/{}-{}.csv", args.ticker, date);

    println!("File: {csv_path}");

    let data_file: File = File::open(&csv_path).expect("File does not exist");

    let data_frame: PolarsResult<DataFrame> = CsvReader::new(data_file)
        .infer_schema(None)
        .has_header(true)
        .finish();

    match data_frame {
        Err(err) => println!("{err}"),
        Ok(mut df) => {
            calculate(&mut df, 1, args.limit);
            // println!("{df}")
        }
    };
}
