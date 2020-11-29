/**
 * @Name: sample_06_04
 * @Description:
 * @CreatedBy: Masato Shima
 * @CreatedOn: 2019/08/28
 **/

"use strict";

let hello = new Vue(
    {
        el: "#hello",
        data: {
            namae: "Masato",
            result: "",
        },
        methods: {
            run: function () {
                this.$http.get(
                    "/get",
                    {
                        "params": {
                            "namae": this.namae,
                        }
                    }
                ).then(
                    response => {
                        this.result = response.body.greet;
                    },
                    response => {
                        // エラー時
                        console.log("NG");
                        console.log(response.body);
                    }
                );
            },
        }
    }
);

// End
