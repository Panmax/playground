/**
 * Created by pan on 16/1/5.
 */

new Vue({
    el: '#music',

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
        musics: null,
        favorite_musics: null
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
            if (this.keyword == 'like') {
                this.fetchMyFavoriteMusics();
                return
            }
            this.addSearchHistory(this.keyword);
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/music/api/get_musics?keyword=' + this.keyword);
            xhr.onload = function () {
                self.favorite_musics = null;
                self.musics = JSON.parse(xhr.responseText)
            };
            xhr.send();
        },
        likeMusic: function (music) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/music/api/music_favorite');
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onload = function () {
                if (xhr.status == 401) {
                    alert('请先登录');
                    return;
                }
                var result = JSON.parse(xhr.responseText);
                if (result.success) {
                    music.is_like = true;
                } else {
                    alert(result.reason)
                }
            };
            xhr.send(JSON.stringify({song_id: music.song_id}));
        },
        cancelLikeMusic: function (music) {
            var xhr = new XMLHttpRequest();
            xhr.open('DELETE', '/music/api/music_favorite');
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onload = function () {
                console.log(xhr.responseText)
                if (xhr.status == 403) {
                    alert('请先登录');
                    return;
                }
                var result = JSON.parse(xhr.responseText);
                if (result.success) {
                    music.is_like = false;
                } else {
                    alert(result.reason)
                }
            };
            xhr.send(JSON.stringify({song_id: music.song_id}));
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
        fetchMyFavoriteMusics: function () {
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/music/api/music_favorite');
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onload = function () {
                if (xhr.status == 401) {
                    alert('请先登录');
                    return;
                }
                self.musics = null;
                self.favorite_musics = JSON.parse(xhr.responseText);
            };
            xhr.send();
        }
    }
});
