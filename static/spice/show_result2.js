// create some data and a ColumnDataSource

var source = new Bokeh.ColumnDataSource({ data: { x: [], y: [] } });


// make the plot
var plot = Bokeh.Plotting.figure({
    title: "BokehJS Plot",
    plot_width: 400,
    plot_height: 400,
    background_fill_color: "#F2F2F7"
});
var count = 0 ;

function Callback_Refresh(){
    source.data.x = [];
    source.data.y = [];
        // var the_x = SimResult["time"];
        var the_x = [2,4] ; 

            // var the_y = SimResult["nodes"][the_nodes_name[i]] ;
         var the_y = [1+count,3+count];
         source.data.x.push(the_x);
        source.data.y.push(the_y);
  count = count+1;
        source.change.emit();
}

plot.multi_line({field:"x"},{field:"y"},{source:source});
// plot.multi_line([[1,2,3],[1,2,3]],[[2,4,6],[7,8,9]]);

Bokeh.Plotting.show(plot,'#bokeh_01');

var RefreshButton = document.createElement("Button");
RefreshButton.appendChild(document.createTextNode("Refresh"));
document.currentScript.parentElement.appendChild(RefreshButton);
RefreshButton.addEventListener("click", Callback_Refresh);