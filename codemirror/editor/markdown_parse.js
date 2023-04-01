self.importScripts("./js/highlight.min.js")
self.importScripts("./js/marked.min.js");
self.importScripts("./js/mermaid.min.js");

// mermaid.initialize()

//mermaid.initialize();

let rendererMD = new marked.Renderer();
//重写heading，添加一个toc方法
rendererMD.heading = function (text, level, raw) {
    var anchor = tocObj.add(text, level);
    return `<a id=${anchor} class="anchor-fix"></a><h${level}>${text}</h${level}>\n`;
};

//将链接重定向到本地后端服务
rendererMD.image = function(href, title, text) {
    return `<img src="http://127.0.0.1:5000?href=${href}" alt="${text}" title="${title ? title : ''}">`
    // return `<img src="href=${href}" alt="${text}" title="${title ? title : ''}">`
}

marked.setOptions({
    renderer: rendererMD,
    gfm: true,//它是一个布尔值，默认为true。允许 Git Hub标准的markdown.
    tables: true,//它是一个布尔值，默认为true。允许支持表格语法。该选项要求 gfm 为true。
    breaks: false,//它是一个布尔值，默认为false。允许回车换行。该选项要求 gfm 为true。
    pedantic: false,//它是一个布尔值，默认为false。尽可能地兼容 markdown.pl的晦涩部分。不纠正原始模型任何的不良行为和错误。
    sanitize: false,//它是一个布尔值，默认为false。对输出进行过滤（清理），将忽略任何已经输入的html代码（标签）
    smartLists: true,//它是一个布尔值，默认为false。使用比原生markdown更时髦的列表。 旧的列表将可能被作为pedantic的处理内容过滤掉.
    smartypants: false//它是一个布尔值，默认为false。使用更为时髦的标点，比如在引用语法中加入破折号。
});

// marked.setOptions({
//     highlight: function (code) {
//         return hljs.highlightAuto(code).value;
//     }
// });

// 结合mermaid语法
marked.setOptions({
    highlight(code, type) {
        if (type === 'mermaid' || type === 'sequence' || type === 'flow') {
            return `<div class="mermaid">${code}</div>`;
        }
        return hljs.highlightAuto(code).value;
        //return hljs.highlight(code,code).value;
    }
})

const tocObj = {
    add: function (text, level) {
        var anchor = `#toc${level}${++this.index}`;
        this.toc.push({anchor: anchor, level: level, text: text});
        return anchor;
    },
    // 使用堆栈的方式处理嵌套的ul,li，level即ul的嵌套层次，1是最外层
    // <ul>
    //   <li></li>
    //   <ul>
    //     <li></li>
    //   </ul>
    //   <li></li>
    // </ul>
    toHTML: function () {
        let levelStack = [];
        let result = '';
        const addStartUL = () => {
            result += '<ul>';
        };
        const addEndUL = () => {
            result += '</ul>\n';
        };
        const addLI = (anchor, text) => {
            result += '<li><a href="#' + anchor + '">' + text + '<a></li>\n';
        };

        this.toc.forEach(function (item) {
            let levelIndex = levelStack.indexOf(item.level);
            // 没有找到相应level的ul标签，则将li放入新增的ul中
            if (levelIndex === -1) {
                levelStack.unshift(item.level);
                addStartUL();
                addLI(item.anchor, item.text);
            } // 找到了相应level的ul标签，并且在栈顶的位置则直接将li放在此ul下
            else if (levelIndex === 0) {
                addLI(item.anchor, item.text);
            } // 找到了相应level的ul标签，但是不在栈顶位置，需要将之前的所有level出栈并且打上闭合标签，最后新增li
            else {
                while (levelIndex--) {
                    levelStack.shift();
                    addEndUL();
                }
                addLI(item.anchor, item.text);
            }
        });
        // 如果栈中还有level，全部出栈打上闭合标签
        while (levelStack.length) {
            levelStack.shift();
            addEndUL();
        }
        // 清理先前数据供下次使用
        this.toc = [];
        this.index = 0;
        return result;
    },
    toc: [],
    index: 0
};


// 执行markdown解析线程
self.addEventListener('message', e => { // 接收到消息
    //console.log(); // Greeting from Main.js，主线程发送的消息
    let content = e.data
    content = marked(content);
    tocHtml = "<div class='toc'><h3>文章目录</h3> " + tocObj.toHTML() + "</div>";
    content = content.replace(/<p>\[Toc]<\/p>/g,tocHtml);
    self.postMessage(content); // 向主线程发送消息
});
