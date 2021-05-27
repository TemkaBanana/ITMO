use csv;
use std::fs::File;
use std::io::{Read, BufReader, BufRead};
use std::path::Path;

fn main() -> Result<(), csv::Error> {
    let f = File::open("/home/alex/github/ITMO/linux_scripting/nginx_logs")?;
    let f = BufReader::new(f);

    let mut res: i64 = 0;
    for line in f.lines() {
        let s: Vec<&str> = line.as_ref().unwrap().split_whitespace().collect();

        match s.get(9).unwrap().parse::<i64>() {
            Ok(n) => res += n,
            Err(e) => res += 0,
        }
    }

    println!("Total: {}", res);
    Ok(())
}