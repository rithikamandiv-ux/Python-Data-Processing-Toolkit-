"""
**************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20241502/21815610
 4. Date: 21/11/2025
**************************

"""

from graphics import *
import csv
import math

VALID_YR_MIN, VALID_YR_MAX = 2000, 2025

AIRPORTS = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International",
}

AIRLINES = {
    "BA": "British Airways", "AF": "Air France", "AY": "Finnair",
    "KL": "KLM", "SK": "Scandinavian Airlines", "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines", "W6": "Wizz Air", "U2": "easyJet",
    "FR": "Ryanair", "A3": "Aegean Airlines", "SN": "Brussels Airlines",
    "EK": "Emirates", "QR": "Qatar Airways", "IB": "Iberia", "LH": "Lufthansa",
}

data_list = []
def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Exiting.")
        raise SystemExit


def load_csv(CSV_chosen):
    # Load CSV file
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

def prompt_city_code() -> str:
    # Validate airport code
    while True:
        raw = safe_input("Please enter the three-letter code for the departure city required:").strip().upper()
        if len(raw) != 3:
            raw = safe_input("Wrong code length - please enter a three-letter city code:").strip().upper()
            if len(raw) != 3:
                continue
        if raw not in AIRPORTS:
            raw = safe_input("Unavailable city code - please enter a valid city code:").strip().upper()
            if raw not in AIRPORTS:
                continue
        return raw

def prompt_year() -> int:
    # Validate year
    while True:
        raw = safe_input("Please enter the year required in the format YYYY:").strip()
        if not (raw.isdigit() and len(raw) == 4):
            raw = safe_input("Wrong data type - please enter a four-digit year value:").strip()
            if not (raw.isdigit() and len(raw) == 4):
                continue
        year = int(raw)
        if not (VALID_YR_MIN <= year <= VALID_YR_MAX):
            raw = safe_input(f"Out of range - please enter a value from {VALID_YR_MIN} to {VALID_YR_MAX}:").strip()
            if not (raw.isdigit() and len(raw) == 4):
                continue
            year = int(raw)
            if not (VALID_YR_MIN <= year <= VALID_YR_MAX):
                continue
        return year
        

def hour_from_hhmm(t: str) -> int:
    # Extract hour
    if not t or ":" not in t: 
        return -1
    hh = t.split(":", 1)[0]
    return int(hh) if hh.isdigit() else -1

def parse_temp_c(weather: str):
    # Extract temperature
    if not weather:
        return None

    start = None
    for i, ch in enumerate(weather):
        if ch.isdigit() or (ch == '-' and i + 1 < len(weather) and weather[i+1].isdigit()):
            start = i
            break

    if start is None:
        return None

    num = ""
    for ch in weather[start:]:
        if ch.isdigit() or ch == "-":
            num += ch
        else:
            break

    try:
        return int(num)
    except:
        return None

def is_rain(weather: str) -> bool:
    return bool(weather) and ("rain" in weather.lower())

def is_delayed(sched: str, actual: str) -> bool:
    # Check delay
    return bool(sched and actual and actual > sched)

def compute_outcomes(data_list):
    # Column indices
    C_AIRPORT     = 0
    C_FLIGHT      = 1
    C_SCHED_DEP   = 2
    C_ACT_DEP     = 3
    C_DEST        = 4
    C_DIST        = 5
    C_SCHED_ARR   = 6
    C_ACT_ARR     = 7
    C_TERM        = 8
    C_RUNWAY      = 9
    C_WEATHER     = 10

    # Initialize counters
    total = len(data_list)
    term2 = 0
    under600 = 0
    af_total = 0
    af_delayed = 0
    temp_below15 = 0
    ba_total = 0

    # Initialize dictionaries
    dest_count = {}
    rainy_hours_set = set()
    hour_counts_by_airline = {}
    seen_hours = []
    hour_to_bucket = {}

    for row in data_list:
        # Extract fields
        flight    = row[C_FLIGHT].strip()
        sched_dep = row[C_SCHED_DEP].strip()
        act_dep   = row[C_ACT_DEP].strip()
        dest      = row[C_DEST].strip().upper()
        dist_str  = row[C_DIST].strip()
        term      = row[C_TERM].strip()
        weather   = row[C_WEATHER].strip()

        # Get airline
        airline = flight[:2].upper() if len(flight) >= 2 else ""

        # Terminal 2
        if term == "2":
            term2 += 1

        # Under 600
        try:
            if int(dist_str) < 600:
                under600 += 1
        except ValueError:
            pass

        # Air France
        if airline == "AF":
            af_total += 1
            if is_delayed(sched_dep, act_dep):
                af_delayed += 1

        if airline == 'BA':
            ba_total = ba_total + 1
            if is_delayed(sched_dep, act_dep):
                ba_delayed = ba_delayed + 1

            

        # British Airways
        if airline == "BA":
            ba_total += 1

        # Low temperature
        temp_val = parse_temp_c(weather)
        if temp_val is not None and temp_val < 15:
            temp_below15 += 1

        # Hour processing
        hour = hour_from_hhmm(sched_dep)
        if hour != -1:
            # Rainy hours
            if is_rain(weather):
                rainy_hours_set.add(hour)

            # Hour mapping
            if hour not in hour_to_bucket and len(seen_hours) < 12:
                hour_to_bucket[hour] = len(seen_hours)
                seen_hours.append(hour)

            # Hour counts
            if hour in hour_to_bucket:
                if airline not in hour_counts_by_airline:
                    hour_counts_by_airline[airline] = [0] * 12
                bucket_index = hour_to_bucket[hour]
                hour_counts_by_airline[airline][bucket_index] += 1

        # Destination count
        dest_full = AIRPORTS.get(dest, dest)
        if dest_full not in dest_count:
            dest_count[dest_full] = 0
        dest_count[dest_full] += 1

    # Calculate averages
    if total > 0:
        avg_ba_per_hour = round(ba_total / 12.0, 2)
        pct_ba = round((ba_total / float(total)) * 100.0, 2)
    else:
        avg_ba_per_hour = 0.0
        pct_ba = 0.0

    # AF delay percentage
    if af_total > 0:
        pct_af_delayed = round((af_delayed / float(af_total)) * 100.0, 2)
    else:
        pct_af_delayed = 0.0

    rainy_hours = len(rainy_hours_set)

    # Least destinations
    least_list = []
    if dest_count:
        min_val = min(dest_count.values())
        for name, count in dest_count.items():
            if count == min_val:
                least_list.append(name)
        least_list.sort()

    return {
        "total": total,
        "term2": term2,
        "under600": under600,
        "af_total": af_total,
        "temp_below15": temp_below15,
        "avg_ba_per_hour": avg_ba_per_hour,
        "pct_ba": pct_ba,
        "pct_af_delayed": pct_af_delayed,
        "rainy_hours": rainy_hours,
        "least_destinations": least_list,
        "hour_counts_by_airline": hour_counts_by_airline,
        "hour_labels": seen_hours,
    }

def get_airline_hour_counts(outcomes: dict, airline_code: str):
    # Get hour counts
    counts = outcomes["hour_counts_by_airline"].get(airline_code, [0]*12)
    labels = outcomes["hour_labels"] or list(range(12))
    if len(labels) < 12:
        labels = labels + [""]*(12 - len(labels))
    return counts, labels

def render_histogram(city: str, year: int, airline_code: str, outcomes: dict):
    airline_name = AIRLINES[airline_code]
    airport_name = AIRPORTS[city]
    counts, hour_labels = get_airline_hour_counts(outcomes, airline_code)
    max_val = max(counts) if counts else 0

    # Window dimensions
    W, H = 1024, 768
    left, right = 120, 960
    top, bottom = 120, 80
    n = 12
    slot_h = (H - top - bottom) / n
    bar_gap = 8
    bar_h = max(1, slot_h - bar_gap)
    avail_w = right - left - 40
    scale = (avail_w / max_val) if max_val > 0 else 0

    # Create window
    win = GraphWin("Histogram", W, H)
    win.setBackground(color_rgb(28, 150, 197))

    # Draw title
    title = Text(Point(W/2, 50), f"{airline_name} – {airport_name} {year}")
    title.setSize(16); title.setStyle("bold"); title.setTextColor(color_rgb(207,236,247))
    title.draw(win)

    # Draw axis
    axis = Line(Point(left, top), Point(left, H - bottom))
    axis.setOutline("white"); axis.setWidth(1); axis.draw(win)

    # Draw bars
    for i, val in enumerate(counts):
        y_top = top + i * slot_h + (slot_h - bar_h)/2
        y_bot = y_top + bar_h
        length = int(val * scale)

        # Hour label
        label = str(hour_labels[i]) if i < len(hour_labels) else str(i)
        yl = Text(Point(left - 30, (y_top + y_bot)/2), label)
        yl.setSize(10); yl.setStyle("bold"); yl.setTextColor("white")
        yl.draw(win)

        # Bar rectangle
        x1, x2 = left + 1, left + 1 + length
        rect = Rectangle(Point(x1, y_top), Point(x2, y_bot))
        rect.setOutline("white"); rect.setFill(color_rgb(32, 197, 176))
        rect.draw(win)

        # Value text
        vt = Text(Point(x2 + 14, (y_top + y_bot)/2), str(val))
        vt.setStyle("bold"); vt.setTextColor(color_rgb(207,236,247))
        vt.draw(win)

    # Wait for window close
    while not win.isClosed():
        update(30)

def print_outcomes(city: str, year: int, selected_file: str, o: dict):
    print("*" * 70)
    print(f"File {selected_file} selected - Planes departing {AIRPORTS[city]} {year}")
    print("*" * 70 + "\n")
    print(f"The total number of flights from this airport was {o['total']}")
    print(f"The total number of flights departing Terminal Two was {o['term2']}")
    print(f"The total number of departures on flights under 600 miles was {o['under600']}")
    print(f"There were {o['af_total']} Air France flights from this airport")
    print(f"There were {o['temp_below15']} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {o['avg_ba_per_hour']:.2f} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {o['pct_ba']:.2f}% of all departures")
    print(f"{o['pct_af_delayed']:.2f}% of Air France departures were delayed")
    print(f"There were {o['rainy_hours']} hours in which rain fell")
    label = "destination is" if len(o['least_destinations']) == 1 else "destinations are"
    print(f"The least common {label} {o['least_destinations']}\n")

def append_results_txt(city: str, year: int, selected_file: str, o: dict, path="results.txt"):
    # File handling - append mode  
    with open(path, "a", encoding="utf-8") as f:
        f.write("*" * 70 + "\n")
        f.write(f"File {selected_file} selected - Planes departing {AIRPORTS[city]} {year}\n")
        f.write("*" * 70 + "\n\n")

        f.write(f"    The total number of flights from this airport was {o['total']}\n")
        f.write(f"    The total number of flights departing Terminal Two was {o['term2']}\n")
        f.write(f"    The total number of departures on flights under 600 miles was {o['under600']}\n")
        f.write(f"    There were {o['af_total']} Air France flights from this airport\n")
        f.write(f"    There were {o['temp_below15']} flights departing in temperatures below 15 degrees\n")
        f.write(f"    There was an average of {o['avg_ba_per_hour']:.2f} British Airways flights per hour from this airport\n")
        f.write(f"    British Airways planes made up {o['pct_ba']:.2f}% of all departures\n")
        f.write(f"    {o['pct_af_delayed']:.2f}% of Air France departures were delayed\n")
        f.write(f"    There were {o['rainy_hours']} hours in which rain fell\n")

        # least common destination(s)
        if len(o['least_destinations']) == 1:
            f.write(f"    The least common destination is {o['least_destinations'][0]}\n")
        else:
            f.write(f"    The least common destinations are {o['least_destinations']}\n")

        f.write("\n")

def prompt_airline_code() -> str:
    # Get airline code
    while True:
        raw = safe_input("Enter a two-character Airline code to plot a histogram:").strip().upper()
        if raw in AIRLINES:
            return raw
        raw = safe_input("Unavailable Airline code please try again:").strip().upper()
        if raw in AIRLINES:
            return raw

def prompt_continue() -> bool:
    # Ask if user wants to continue
    while True:
        response = safe_input("\nDo you want to load another CSV file? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        else:
            exit
            
    

# Main loop
def main():
    while True:
        # ---------- Task A: get valid inputs AND a real file ----------
        while True:
            data_list.clear()
            city = prompt_city_code()
            year = prompt_year()
            selected_data_file = f"{city}{year}.csv"

            try:
                load_csv(selected_data_file)      # try to open + load
                break                             # success -> leave inner loop
            except FileNotFoundError:
                print("there is no file in that name. enter a correct name.\n")
                # inner while repeats, asks city + year again

        # ---------- Now we KNOW the file exists ----------
        print("\n" + "*" * 76)
        print(f"File {selected_data_file} selected - "
              f"Planes departing {AIRPORTS[city]} {year}")
        print("*" * 76 + "\n")

        outcomes = compute_outcomes(data_list)
        print_outcomes(city, year, selected_data_file, outcomes)
        append_results_txt(city, year, selected_data_file, outcomes)

        airline = prompt_airline_code()
        render_histogram(city, year, airline, outcomes)

        # ---------- Task E: ask if user wants another CSV ----------
        if not prompt_continue():        # your yes/no function
            break


if __name__ == "__main__":
    main()

"""


References:
  

1. File Handling (Reading and Writing Files):
   - W3Schools - Python File Handling: https://www.w3schools.com/python/python_file_handling.asp
   
2. String Manipulation:
   - W3Schools - Python String Methods: https://www.w3schools.com/python/python_strings_methods.asp

3. Error and Exception Handling:
   - W3Schools - Python Try...Except: https://www.w3schools.com/python/python_try_except.asp

4. Type Hinting:
   - Python Documentation - Type Hints: https://docs.python.org/3/library/typing.html
 
"""
  
