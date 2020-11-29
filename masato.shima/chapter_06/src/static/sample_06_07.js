/**
 * @Name: sample_06_07
 * @Description:
 * @CreatedBy: Masato Shima
 * @CreatedOn: 2019/08/28
 **/

"use strict";

const bartLocation = "/file/third/brat";

head.js(
    // External libraries
    bartLocation + "/client/lib/jquery.min.js",
    bartLocation + "/client/lib/jquery.svg.min.js",
    bartLocation + "/client/lib/jquery.svgdom.min.js",

    // Brat helper modules
    bartLocation + "/client/src/configuration.js",
    bartLocation + "/client/src/util.js",
    bartLocation + "/client/src/annotation_log.js",
    bartLocation + "/client/lib/webfont.js",

    // Brat helper modules
    bartLocation + "/client/src/dispatcher.js",
    bartLocation + "/client/src/url_monitor.js",
    bartLocation + "/client/src/visualizer_ui.js",
);

let brat_dispatcher = undefined;

head.ready(
    function () {
        brat_dispatcher = Util.embed("brat", {}, {"text": ""}, []);
    }
);

let brat = new Vue(
    {
        el: "#brat",
        data: {},
        methods: {
            run: function () {
                this.$http.get(
                    "/get",
                    {
                        "params": {}
                    }
                ).then(
                    response => {
                        brat_dispatcher.post(
                            "collectionLoaded",
                            [response.body.collection]
                        );
                        brat_dispatcher.post(
                            "requestRenderData",
                            [response.body.annotation]
                        );
                    },
                    response => {
                        console.log("NG");
                        console.log(response.body);
                    }
                )
            }
        }
    }
);

// End
