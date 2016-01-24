/**
 * Created by pan on 16/1/5.
 */

new Vue({
    el: '#app',

    data: {
        play_url: '',
        is_playing: false,
        as: audiojs.createAll({
                trackEnded: function () {
                    audio.load(url);
                    audio.play()
                }
            }),
        keyword: '',
        musics: null
    },

    created: function () {
        //this.checkIsLogin()
    },

    watch: {
    },

    methods: {
        playMusic: function (url) {
            this.play_url = url;
            this.is_playing = true;
            var audio = this.as[0];
            audio.load(url);
            audio.play();
            console.log(this.play_url)
        },
        downLoad: function (url) {
            window.open(url)
        },
        searchMusic: function () {
            this.addSearchHistory(this.keyword);
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/music/api/get_musics?keyword=' + this.keyword);
            xhr.onload = function () {
                self.musics = JSON.parse(xhr.responseText)
            };
            xhr.send();
        },
        likeMusic: function (song_id) {
            for(i in this.musics) {
                if(this.musics[i].song_id == song_id) {
                    this.musics[i].is_like = true
                }
            }
        },
        cancelLikeMusic: function (song_id) {
            for(i in this.musics) {
                if(this.musics[i].song_id == song_id) {
                    this.musics[i].is_like = false
                }
            }
        },
        addSearchHistory: function (keyname) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/music/api/music_search_history');
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            //xhr.onload = function () {
            //    alert(xhr.responseText)
            //};
            xhr.send(JSON.stringify({keyword: keyname}));
        },
        checkIsLogin: function () {
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/music/api/user_info');
            xhr.onload = function () {
                alert(xhr.responseText)
            };
            xhr.send();
        }
    }
});
