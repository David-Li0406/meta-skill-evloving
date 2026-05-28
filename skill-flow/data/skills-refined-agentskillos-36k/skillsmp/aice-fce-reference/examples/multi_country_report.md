# Complex Report Example: Multi-Country Evaluation

This example demonstrates how to generate references for a report containing credentials from multiple countries (Hong Kong, UK) and different years, including official website citations.

## Scenario
**User Credentials:**
1.  Bachelor of Science, HKUST (Hong Kong), 2014.
2.  Master of Philosophy, University of Cambridge (UK), 2018.
3.  Doctor of Philosophy, University of Hong Kong (Hong Kong), 2020.

## Step 1: Lookup Standard References (APA)

### Command 1 (HKUST, 2014)
```bash
python scripts/lookup_refs.py --context "Hong Kong Bachelor" --year 2014
```
**Output:**
*   International Association of Universities (IAU). (2009). *International Handbook of Universities* (21st). Palgrave Macmillan.
*   Europa Publications. (2011). *The Europa World of Learning* (62nd). Routledge.

### Command 2 (Cambridge, 2018)
```bash
python scripts/lookup_refs.py --context "United Kingdom Master" --year 2018
```
**Output:**
*   Peterson's. (2020). *Peterson's Graduate Programs Series* (55th).

### Command 3 (General/Transcript Guide)
*Typically added for all reports.*
**Output:**
*   AACRAO. (2011). *AACRAO Academic Record and Transcript Guide* (1st (2011)).

## Step 2: Generate Website Citations

### Command 4 (HKUST)
```bash
python scripts/lookup_refs.py --make-citation "The Hong Kong University of Science and Technology" "https://hkust.edu.hk"
```
**Output:**
*   The Hong Kong University of Science and Technology. (n.d.). *Home Page*. Retrieved from https://hkust.edu.hk

### Command 5 (Cambridge)
```bash
python scripts/lookup_refs.py --make-citation "University of Cambridge" "https://www.cam.ac.uk"
```
**Output:**
*   University of Cambridge. (n.d.). *Home Page*. Retrieved from https://www.cam.ac.uk

### Command 6 (HKU)
```bash
python scripts/lookup_refs.py --make-citation "The University of Hong Kong" "https://www.hku.hk"
```
**Output:**
*   The University of Hong Kong. (n.d.). *Home Page*. Retrieved from https://www.hku.hk

## Final Combined Output (React/HTML)

```jsx
<ul className="list-disc pl-4 space-y-1 text-gray-600">
  <li>International Association of Universities (IAU). (2009). <em>International Handbook of Universities</em> (21st). Palgrave Macmillan.</li>
  <li>Europa Publications. (2011). <em>The Europa World of Learning</em> (62nd). Routledge.</li>
  <li>AACRAO. (2011). <em>AACRAO Academic Record and Transcript Guide</em> (1st (2011)).</li>
  <li>Peterson's. (2020). <em>Peterson's Graduate Programs Series</em> (55th).</li>
  <li>The Hong Kong University of Science and Technology. (n.d.). <em>Home Page</em>. (<a href="https://hkust.edu.hk" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">https://hkust.edu.hk</a>)</li>
  <li>University of Cambridge. (n.d.). <em>Home Page</em>. (<a href="https://www.cam.ac.uk" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">https://www.cam.ac.uk</a>)</li>
  <li>The University of Hong Kong. (n.d.). <em>Home Page</em>. (<a href="https://www.hku.hk" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">https://www.hku.hk</a>)</li>
</ul>
```
