
editor.on("change", function(mc) {
    // console.log(mc.doc.getValue());
    // 把内容交给子线程解析
    let content = mc.doc.getValue()
    if(content){
        markdown_parse_worker.postMessage(content);
    }
});

// myWorker.postMessage('Greeting from Main.js'); // 向 worker 线程发送消息，对应 worker 线程中的 e.data

document.onload = function (){
    //监听editor改变事件
}

