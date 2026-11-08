# Alternatives — two follow-on projects

## 1. Forecast + safety-stock model (best for planner roles)
- **Question:** How much safety stock do we need for a part family, and at what service level?
- **Data:** DataCo monthly demand by product category, plus a lead-time assumption you state plainly.
- **Method:** forecast demand (moving average / trend), then reorder point = avg daily demand × lead time + safety stock, where safety stock = Z × σ(demand during lead time). Run it at 90%, 95%, and 99% service levels and show the inventory cost trade-off.
- **Deliverable:** a table by part family / service level, plus a short note on what a higher service level costs in inventory.
- **Why it works:** more technical, directly relevant to planning, and it forces you to show assumptions.

## 2. Warehouse slotting / pick-path simulation (best for your current coursework)
- **Question:** How much travel time does ABC slotting save vs. current slotting?
- **Data:** simulated warehouse layout + pick frequencies, or DataCo product / order frequency as a proxy for fast/slow movers.
- **Method:** classify SKUs A/B/C by pick frequency, place A-movers closest to the pick face / dock, simulate pick paths (e.g. S-shape vs. return routing), compare total travel distance / time.
- **Link to coursework:** material handling, storage systems, and ASRS — explain where automation (ASRS) would help and where simple slotting is enough.
- **Deliverable:** a layout diagram, a before/after travel-time table, and a note on what you would not automate yet.
- **Why it works:** connects directly to the storage-systems modules you are taking now, and it is a concrete operations simulation, not just a chart.
