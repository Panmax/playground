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
        }
    }
});