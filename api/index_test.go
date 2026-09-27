package handler

import (
	"encoding/xml"
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"strings"
	"testing"
)

func TestCustomIconsSurviveUpstreamSync(t *testing.T) {
	for _, name := range []string{
		"chainlink", "consul", "docker", "dockerswarm", "fluentd", "flux",
		"istio", "kustomize", "linkerd", "logstash", "packer", "vault", "windows11",
	} {
		for _, theme := range []string{"", "auto", "dark", "light"} {
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+".svg")
			})
		}
	}
}

func TestUpstreamIconsAndAliases(t *testing.T) {
	for _, test := range []struct {
		name, theme, asset string
	}{
		{"chi", "", "chi-auto.svg"},
		{"js", "", "javascript.svg"},
		{"python", "light", "python-light.svg"},
		{"py", "dark", "python-dark.svg"},
		{"sp", "", "adobespark.svg"},
		{"sqla", "", "sqlalchemy-auto.svg"},
		{"notepad++", "light", "notepadpp-light.svg"},
		{"jq", "dark", "jqlang-dark.svg"},
		{"chainlink-light", "", "chainlink-light.svg"},
		{"consul-dark", "", "consul-dark.svg"},
	} {
		t.Run(test.name, func(t *testing.T) {
			assertIconResponse(t, test.name, test.theme, test.asset)
		})
	}
}

func assertIconResponse(t *testing.T, name, theme, asset string) {
	t.Helper()
	expected, err := os.ReadFile("../assets/" + asset)
	if err != nil {
		t.Fatal(err)
	}
	query := url.Values{"i": {name}, "theme": {theme}}
	recorder := httptest.NewRecorder()
	Handler(recorder, httptest.NewRequest(http.MethodGet, "/api/icons?"+query.Encode(), nil))
	if recorder.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", recorder.Code, http.StatusOK)
	}
	if got := recorder.Header().Get("Content-Type"); got != "image/svg+xml" {
		t.Errorf("Content-Type = %q, want image/svg+xml", got)
	}
	if !strings.Contains(recorder.Body.String(), string(expected)) {
		t.Errorf("response does not contain %s", asset)
	}
	decoder := xml.NewDecoder(strings.NewReader(recorder.Body.String()))
	for {
		_, err := decoder.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			t.Fatalf("invalid SVG response: %v", err)
		}
	}
}
