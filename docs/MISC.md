# Misc

## Implementation details

### Station code

- For convenience, instead of the old scheme (e.g. W2, E11), networks before 2001 will use the contemporary station code scheme (e.g. EW14, NS11).
- Likewise, the Changi Airport Branch stations (before TELe conversion) will only use the "CG" line code instead of their old "EW" line codes.

### Travel duration

- The preset travel duration estimates are manually recorded in fair weather conditions.
- Travel durations for defunct segments and future segments are estimates based on their rail path length.
- Train speeds were different in the past, and are expected to change in the future.
- Real travel duration can be affected by bad weather, traffic congestion, ongoing construction works, or train service disruption.
- A trip begins when you board the train at the origin and ends when you alight at your destination. So when calculating the fastest route, any interchange transfer time before and after the trip is excluded (i.e. NS1 -> EW24 -> EW21 -> CC22 will be treated as the same as EW24 -> EW21).
- Dwell time at the end of the journey is also excluded; once you have reached your destination, you no longer care how long the train takes to depart.

### Path distance

- The approximate path distance metric treats adjacent stations as being connected directly by their great-circle distance. Real paths between adjacent stations are not "straight lines", so the actual path distance should be higher. Actual rail path lengths will be used in the future.

## Future stages

These stages are tentative and subject to detailed planning.

### CRL Phase 3

<https://www.straitstimes.com/singapore/possible-interchanges-in-king-albert-park-clementi-jurong-pier-gul-circle-for-cross-island>

- CR20
- CR21/JS12 Jurong Pier
- CR22
- CR23
- CR24/EW30 Gul Circle

### Thomson-East Coast Line Extension (TELe)

<https://www.lta.gov.sg/content/ltagov/en/newsroom/2025/3/news-releases/expanding_our_rail_network_and_strengthening_rail_reliability.html>

- The official name and location coordinates for TE32 Changi Airport Terminal 5 has not been released.

### West Coast Extension

<https://www.lta.gov.sg/content/ltagov/en/newsroom/2025/3/news-releases/expanding_our_rail_network_and_strengthening_rail_reliability.html>

Extends the Jurong Region Line to connect with the Circle Line and Cross Island Line.

### Seletar Line

<https://www.lta.gov.sg/content/ltagov/en/newsroom/2025/3/news-releases/expanding_our_rail_network_and_strengthening_rail_reliability.html>

Serves areas such as Woodlands, Sembawang, Sengkang West, Serangoon North, Whampoa, Kallang, and the Greater Southern Waterfront.

### Tengah Line

<https://www.lta.gov.sg/content/ltagov/en/newsroom/2025/3/news-releases/expanding_our_rail_network_and_strengthening_rail_reliability.html>

Serves areas such as Tengah, Bukit Batok, Queensway, and Bukit Merah.
