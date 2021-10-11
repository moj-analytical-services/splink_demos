import json
from IPython.display import display, Javascript, Markdown, HTML
import ipywidgets as widgets


def link_data_with_tooltip(
    df,
    source_field="src",
    target_field="dst",
    cols_to_retain=[],
    cols_to_drop_from_tooltip=[],
    cluster_id=None,
    cluster_field="cluster_id",
):
    if cluster_id:
        df = df[df[cluster_field] == cluster_id]

    recs = df.to_dict(orient="records")
    new_recs = []
    for r in recs:
        new_row = {}

        for c in cols_to_retain:
            new_row[c] = r[c]
            new_row["source"] = r[source_field]
            new_row["target"] = r[target_field]

        tooltip_cols = [c for c in r.keys() if c not in cols_to_drop_from_tooltip]
        tooltip = {}
        for c in tooltip_cols:
            tooltip[c] = r[c]
        new_row["tooltip"] = tooltip
        new_recs.append(new_row)
    return new_recs


def node_data_with_tooltip(
    df,
    cols_to_retain=["cluster_id"],
    cols_to_drop_from_tooltip=[],
    cluster_id=None,
    cluster_field="cluster_id",
):
    if cluster_id:
        df = df[df[cluster_field] == cluster_id]

    recs = df.to_dict(orient="records")
    new_recs = []
    for r in recs:
        new_row = {}

        for c in cols_to_retain:
            new_row[c] = r[c]

        tooltip_cols = [c for c in r.keys() if c not in cols_to_drop_from_tooltip]
        tooltip = {}
        for c in tooltip_cols:
            tooltip[c] = r[c]
        new_row["tooltip"] = tooltip
        new_recs.append(new_row)
    return new_recs


def get_html_cluster_metrics(graphstats_row_as_df):
    c = graphstats_row_as_df.to_dict(orient="records")[0]
    c["radius"] = None
    table = """
    <h2>Cluster {cluster_id}</h2>
    <table>
      <tr>
        <th style="text-align:left">Metric</th>
        <th>Value</th>
        <th style="text-align:left">Description</th>
      </tr>
      <tbody>

      <tr>
        <td style="text-align:left">Diameter</td>
        <td>{diameter}</td>
        <td style="text-align:left">The <b>diameter</b> of a graph is the longest path between any two nodes.</td>
      </tr>


      <tr>
        <td style="text-align:left">Radius</td>
        <td>{radius}</td>
                <td style="text-align:left">The <b>radius</b> is the largest distance from node at the centre of a graph to the edge of the graph.  </td>
      </tr>

      <tr>
        <td style="text-align:left">Density</td>
        <td>{density:,.3f}</td>
                <td style="text-align:left">The <a href="https://bookdown.org/omarlizardo/_main/2-9-density.html"><b>density</b></a> is a mesure of interconnectedness. It is defined by the number of edges divided by the number of possible edges.</td>
      </tr>

      <tr>
        <td style="text-align:left">Transitivity</td>
        <td>{transitivity:,.3f}</td>
                <td style="text-align:left">The <b>transitivity</b> is the overall probability for the network to have adjacent nodes interconnected. Higher transitivity indicates more tightly connected groups of nodes.</td>
      </tr>

      <tr>
        <td style="text-align:left">Triangle cluster coefficient</td>
        <td>{tri_clustcoeff:,.3f}</td>
                <td style="text-align:left"></td>
      </tr>

      <tr>
        <td style="text-align:left">Square cluster coefficient</td>
        <td>{sq_clustcoeff:,.3f}</td>
                <td style="text-align:left"></td>
      </tr>


      </tbody>
    </table>
    """
    return table.format(**c)


def display_outputs(
    cluster_id,
    df_e,
    nodestats,
    graphstats,
    edge_metric="edge_betweenness",
    start_width=500,
    start_height=500,
):

    link_data = link_data_with_tooltip(
        df_e,
        cluster_id=cluster_id,
        cols_to_retain=["weight", "edge_betweenness"],
        cols_to_drop_from_tooltip=["cluster_id", "src", "dst", "group_l", "group_r"],
    )

    node_data = node_data_with_tooltip(
        nodestats,
        cols_to_retain=["cluster_id", "eigen_centrality", "node_id"],
        cluster_id=cluster_id,
    )

    with open("data/graph/force_template.vg.json") as f:
        vl = json.load(f)
    vl["data"][0] = {"name": "node-data", "values": node_data}

    vl["data"][1] = {"name": "link-data", "values": link_data}

    vl["signals"][4]["value"] = start_height
    vl["signals"][5]["value"] = start_width

    if edge_metric == "weight":
        vl["scales"][1]["domain"]["field"] = "weight"

        vl["scales"][1]["reverse"] = True
        vl["marks"][1]["encode"]["update"]["stroke"]["field"] = "weight"

        # Scale 3 is edge_length_scale
        vl["scales"][3]["domain"] = {"data": "link-data", "field": "weight"}
        vl["scales"][3]["reverse"] = False

        vl["marks"][0]["transform"][0]["forces"][3]["distance"][
            "expr"
        ] = "scale('edge_length_scale',datum.weight)*linkDistance"

    script = f"""
       var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//cdn.jsdelivr.net/npm/vega@5';
        document.head.appendChild(script);

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//cdn.jsdelivr.net/npm/vega-embed@6';
        document.head.appendChild(script);

        var spec = `{json.dumps(vl, default=convert)}`
        spec= JSON.parse(spec)
        vegaEmbed(element, spec).then(function(result) {{
          }}).catch(console.error);
    """

    display(
        HTML(
            """
    <style>
    .jupyter-widgets {

     overflow: auto !important;
    }
    </style>
    """
        )
    )
    html = get_html_cluster_metrics(graphstats[graphstats["cluster_id"] == cluster_id])
    display(HTML(html))

    display(Javascript(script))
    display(Markdown("### Nodes"))
    display(nodestats[nodestats["cluster_id"] == cluster_id])
    display(Markdown("### Edges"))
    display(df_e[df_e["cluster_id"] == cluster_id])
    # display(print(json.dumps(vl,indent=4)))
    
    with open('vega_spec_with_data.vg.json', 'w') as f:
        json.dump(vl, f, default=convert)
    


def get_dd_cluster_id(df_nodestats):
    dd_values = sorted(list(df_nodestats["cluster_id"].unique()))

    dd_cluster_id = widgets.Dropdown(
        options=dd_values,
        value=dd_values[0],
        description="Cluster:",
    )

    return dd_cluster_id


def get_interface(df_e, df_nodestats, df_graphstats, start_width=500, start_height=500):
    def on_change(change):
        output.clear_output()
        cluster_id = dd_cluster_id.value
        edge_metric = dd_edge_metric.value

        with output:
            display_outputs(
                cluster_id,
                df_e,
                df_nodestats,
                df_graphstats,
                edge_metric=edge_metric,
                start_width=start_width,
                start_height=start_height,
            )

    output = widgets.Output()

    dd_cluster_id = get_dd_cluster_id(df_nodestats)

    dd_edge_metric = widgets.RadioButtons(
        description="Edge metric", options=["edge_betweenness", "weight"]
    )

    dd_cluster_id.observe(on_change, names="value")
    dd_edge_metric.observe(on_change, names="value")

    display(dd_cluster_id)
    display(dd_edge_metric)
    display(output)
    on_change(None)


def convert(o):
    if "NA" in repr(type(o)):
        return None
    else:
        return int(o)
