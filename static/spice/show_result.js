/*  基于bokeh.js库文件
    使用该文件前请现在html加载相关js文件*/

// 仿真结果数据
var SimResult ;
var Flag_Refresh = false ;

var color_store = ["blue","brown","cyan","green","orange","pink","purple","red","whitesmoke","yellow"];
// create a data source to hold data
var the_source = new Bokeh.ColumnDataSource({
    data: { x: [], y: [], color: [] }
});



// make a plot with some tools
var plot = Bokeh.Plotting.figure({
    title:'Example of Random data',
    tools: "pan,wheel_zoom,box_zoom,reset,save",
    height: 300,
    width: 400,
    background_fill_color: "#F2F2F7"
});


function plotPoint() {

    if(Flag_Refresh == true){
        
        the_source.data.x = [];
        the_source.data.y = [];
        the_source.data.color = [];


        console.log("Flag_Refresh = true !");
        var the_nodes_name = SimResult["nodes_name"];

        var the_x = SimResult["time"];
        for(var i=0; i < the_nodes_name.length; i++){
            var the_y = SimResult["nodes"][the_nodes_name[i]] ;
            the_source.data.x.push(the_x);
            the_source.data.y.push(the_y);
            the_source.data.color.push(color_store[i%color_store.length]);
        }
        the_source.change.emit();

    }
}



function requestSimInfo(){
    var data = new Object();
    var sim_result ;

    data["sim_type"] = 'transient';

    $.ajax({
        type: 'POST',
        url: "/getsiminfo",
        data: data,
        async:false,    // 必须关闭异步！！！
        dataType:'json',
        success: function (siminfo) {
            console.log("load sim result successfully !!");
            sim_result = siminfo;
        },
        error: function(){
            alert('failed');
        }
    });    
    return sim_result ;
}



function Callback_PlotPoint() {

    plotPoint();
}

function Callback_Refresh(){
    SimResult = requestSimInfo();
    Flag_Refresh = true;
}




// add a line with data from the source
plot.multi_line({field:"x"},{field:"y"},{
    source: the_source,
    color: {field:"color"},
    line_width: 2
});



// show the plot, appending it to the end of the current section
Bokeh.Plotting.show(plot,'#bokeh_01');



var RefreshButton = document.createElement("Button");
RefreshButton.appendChild(document.createTextNode("Refresh"));
document.currentScript.parentElement.appendChild(RefreshButton);
RefreshButton.addEventListener("click", Callback_Refresh);

var addDataButton = document.createElement("Button");
addDataButton.appendChild(document.createTextNode("Plot"));
document.currentScript.parentElement.appendChild(addDataButton);
addDataButton.addEventListener("click", Callback_PlotPoint);
