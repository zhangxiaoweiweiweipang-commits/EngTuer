package com.xw.englishreader;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.util.Locale;

/**
 * 一个极简的 WebView 壳：
 *  - 加载 assets/index.html（完全离线，不联网）
 *  - 把安卓系统的 TextToSpeech 暴露给网页，用来朗读英文
 *  - 接管返回键，交给网页自己决定是后退还是退出
 */
public class MainActivity extends Activity {

    private WebView web;
    private TextToSpeech tts;
    private volatile boolean ttsReady = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        tts = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int r = tts.setLanguage(Locale.US);
                    ttsReady = (r != TextToSpeech.LANG_MISSING_DATA
                             && r != TextToSpeech.LANG_NOT_SUPPORTED);
                    tts.setSpeechRate(0.85f);
                }
            }
        });

        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);      // localStorage 存学习进度，必须开
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setTextZoom(100);                // 不跟随系统字体缩放，App 内自己调字号
        web.setWebViewClient(new WebViewClient());
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        web.addJavascriptInterface(new TtsBridge(), "AndroidTTS");
        web.loadUrl("file:///android_asset/index.html");

        setContentView(web);
    }

    /** 网页里通过 window.AndroidTTS 调用 */
    public class TtsBridge {
        @JavascriptInterface
        public boolean available() {
            return ttsReady;
        }

        @JavascriptInterface
        public void speak(String text) {
            if (tts == null || !ttsReady || text == null) return;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "yy");
            } else {
                tts.speak(text, TextToSpeech.QUEUE_FLUSH, null);
            }
        }

        @JavascriptInterface
        public void stop() {
            if (tts != null) tts.stop();
        }
    }

    @Override
    public void onBackPressed() {
        if (web == null) { super.onBackPressed(); return; }
        web.evaluateJavascript(
            "(function(){try{return window.androidBack ? androidBack() : false;}catch(e){return false;}})()",
            new ValueCallback<String>() {
                @Override
                public void onReceiveValue(String value) {
                    if (!"true".equals(value)) finish();
                }
            });
    }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); tts = null; }
        if (web != null) { web.destroy(); web = null; }
        super.onDestroy();
    }
}
