import os


def generate_html(png_files, png_dir, plots_per_row=4, output_html="view_plots.html",
                  random_per_block=None, block_size=100, nth_interval=None):
    """
    Generate an HTML file to view PNG plots in a grid layout.

    Parameters:
    - png_files (list of str): list of PNG filenames (e.g., ['a.png', 'b.png'])
    - png_dir (str or Path): path to the directory containing the PNG files
    - plots_per_row (int): number of plots to show per row
    - output_html (str): path to output HTML file
    - random_per_block (int or None): if set, randomly select this many plots in
      every ``block_size`` plots
    - block_size (int): size of the block used for ``random_per_block``
    - nth_interval (int or None): if set, also include every ``nth_interval``-th
      plot in the HTML output
    """

    html_dir = os.path.dirname(os.path.abspath(output_html))
    png_dir_abs = os.path.abspath(png_dir)
    output_html_abs = os.path.abspath(output_html)

    n_files = len(png_files)
    indices = set()

    if nth_interval and nth_interval > 0:
        indices.update(range(0, n_files, nth_interval))

    if random_per_block and block_size and random_per_block > 0:
        import random
        for start in range(0, n_files, block_size):
            end = min(start + block_size, n_files)
            count = min(random_per_block, end - start)
            indices.update(random.sample(range(start, end), count))

    if indices:
        indices = sorted(indices)
        png_files = [png_files[i] for i in indices]

    png_paths = [os.path.join(png_dir, f) for f in png_files]
    rel_paths = [os.path.relpath(png_path, start=html_dir)
                 for png_path in png_paths]

    html_header = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>PNG Plot Viewer</title>
  <style>
    body {{
      font-family: sans-serif;
      padding: 20px;
    }}

    h1 {{
      font-size: 20px;
      margin-bottom: 10px;
    }}

    .top-link {{
      margin-bottom: 15px;
    }}

    .top-link a {{
      font-size: 16px;
      text-decoration: none;
      color: #0066cc;
    }}

    .path-info {{
      font-size: 14px;
      color: #444;
      margin-bottom: 20px;
    }}

    input {{
      font-size: 16px;
      padding: 5px;
      width: 400px;
      margin-bottom: 20px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat({plots_per_row}, 1fr);
      gap: 20px;
    }}

    .plot {{
      border: 1px solid #ccc;
      padding: 5px;
      text-align: center;
    }}

    .filename {{
      font-weight: bold;
      font-size: 14px;
      margin-bottom: 5px;
      word-break: break-word;
    }}

    img {{
      max-width: 100%;
      height: auto;
      cursor: pointer;
      transition: transform 0.2s;
    }}

    img:hover {{
      transform: scale(1.02);
    }}

    @media (max-width: 1200px) {{
      .grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 600px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>

  <div class="top-link">
    <a href="../">⬆️ Go Up One Directory</a>
  </div>

  <h1>PNG Plot Viewer</h1>

  <div class="path-info">HTML generated at: <code>{output_html_abs}</code></div>
  <div class="path-info">PNG directory: <code>{png_dir_abs}</code></div>

  <input type="text" id="filterInput" placeholder="Filter by filename..." onkeyup="filterPlots()">

  <div id="plotContainer" class="grid">
"""

    html_body = ""
    for filename, rel_path in zip(png_files, rel_paths):
        name_attr = filename.lower().replace(".", "_").replace("/", "_")
        block = f"""    <div class="plot" data-name="{name_attr}">
      <div class="filename">{filename}</div>
      <a href="{rel_path}" target="_blank">
        <img src="{rel_path}" alt="">
      </a>
    </div>
"""
        html_body += block

    html_footer = """  </div>

  <script>
    function filterPlots() {
      const filter = document.getElementById("filterInput").value.toLowerCase();
      const plots = document.getElementsByClassName("plot");

      for (let plot of plots) {
        const name = plot.getAttribute("data-name");
        plot.style.display = name.includes(filter) ? "" : "none";
      }
    }
  </script>

</body>
</html>
"""

    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    with open(output_html, "w") as f:
        f.write(html_header + html_body + html_footer)

    print(f"✅ HTML viewer generated at: {output_html_abs}")
