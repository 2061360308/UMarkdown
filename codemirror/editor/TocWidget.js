function webSort() {
    let userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    let isOpera = userAgent.indexOf("Opera") > -1;
    if (isOpera) {
        return "Opera";
    } //判断是否Opera浏览器
    if (userAgent.indexOf("Firefox") > -1) {
        return "Firefox";
    } //判断是否Firefox浏览器
    if (userAgent.indexOf("Chrome") > -1) {
        return "Chrome";
    }
    if (userAgent.indexOf("Safari") > -1) {
        return "Safari";
    } //判断是否Safari浏览器
    if (userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera) {
        return "IE";//判断是否IE浏览器
    }
}

window.onload = function () {
    if (webSort() === "Firefox") {
        console.log("是FireFox浏览器,启用浏览器调试")
        let color = "#31363b"

        changeStylesheet(
            "theme.css",
            '.cm-s-dracula.CodeMirror',
            'background-color',
            color);
    }
    /*Python留有的接口，通过它调用Python函数*/
    new QWebChannel(qt.webChannelTransport, function (channel) {
        PythonBridge = channel.objects.Bridge  // 获取Qt注册的对象
        console.log(PythonBridge);
    });
}

/* 给Python提供的方法 */

function changeTheme(stylesheetFile) {
    /*
    * 更改theme
    * stylesheetFile: css文件路径
    * */
    function removeStyles(file) {
        let filename = file;
        let targetelement = "link";
        let targetattr = "href";
        let allsuspects = document.getElementsByTagName(targetelement);
        for (let i = allsuspects.length; i >= 0; i--) {
            if (allsuspects[i] && allsuspects[i].getAttribute(targetattr) != null && allsuspects[i].getAttribute(
                targetattr).indexOf(filename) !== -1) {
                allsuspects[i].parentNode.removeChild(allsuspects[i]);
            }
        }
    }

    function loadStyles(file) {
        let headElm = document.getElementsByTagName("head")[0];
        let fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", file);
        headElm.appendChild(fileref);
    }

    removeStyles(stylesheetFile)
    loadStyles(stylesheetFile)
}

function updateToc(toc){
    console.log(toc);
    tocEml.innerHTML = toc.data;
}
