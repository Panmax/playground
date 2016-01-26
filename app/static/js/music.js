/**
 * Created by pan on 16/1/5.
 */

new Vue({
    el: '#music',

    data: {
        play_url: '',
        is_playing: false,
        ap: new APlayer({
            element: document.getElementById('player'),
            narrow: false,
            autoplay: false,
            showlrc: false,
            theme: '#e6d0b2',
            music: {
                title: 'Preparation',
                author: 'Hans Zimmer',
                url: 'http://ac-0szrvxda.clouddn.com/0d18477ac0cec0fb.mp3',
                pic: 'http://ac-0szrvxda.clouddn.com/a88762ec37c5efdd.jpg'
            }
        }),
        keyword: '',
        musics: null,
        favorite_musics: null
    },

    created: function () {
        this.ap.init();
    },

    watch: {
    },

    methods: {
        playMusic: function (music, from) {
            if (from == 'xiami') {
                this.ap.music.url = music.audition_list[music.audition_list.length-1].url;
                this.ap.music.title = music.song_name;
                this.ap.music.author = music.singer_name;
                this.ap.music.pic = null;
                if (music.hasOwnProperty('mv_list')) {
                    this.ap.music.pic = music.mv_list[0].pic_url;
                }
                this.ap.init();
            } else if(from == 'me') {
                this.ap.music.url = music.url;
                this.ap.music.title = music.song_name;
                this.ap.music.author = music.singer_name;
                this.ap.music.pic = null;
                if (music.hasOwnProperty('pic_url') &&  music.pic_url != '') {
                    this.ap.music.pic = music.pic_url;
                }
                this.ap.init();
            }
        },
        downLoad: function (url) {
            window.open(url)
        },
        searchMusic: function () {
            $('#searchModal').modal('hide');
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
        },
        clickSearchBtn: function () {
            $('#searchModal').modal('show');
            $('#searchModal').on('shown.bs.modal', function () {
                $('#searchInput').focus();
            });
        }
    }
});
