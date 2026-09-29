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
		"consul", "docker", "fluentd", "flux",
		"istio", "kustomize", "linkerd", "logstash", "packer", "vault",
		"kubernetes", "prometheus", "debian", "ubuntu", "c", "dotnet",
		"discord", "kafka", "postman", "solidity",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}

	for _, name := range []string{"chainlink", "windows11"} {
		for _, theme := range []string{"", "auto"} {
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

func TestNewProposedIcons(t *testing.T) {
	for _, name := range []string{
		"terragrunt", "crossplane", "rke2", "cilium", "kuma",
		"loki", "tempo", "harbor", "minio", "longhorn",
		"externalsecrets", "falco", "trivy", "certmanager", "vmware",
		"opentofu", "kubescape", "mimir", "pyroscope",
		"arm", "alloy", "envoy", "dynatrace", "keepalived", "tekton",
		"claudecode", "codex", "antigravity", "ossfuzz",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}

	for _, alias := range []struct {
		input, target string
	}{
		{"cert-manager", "certmanager-auto.svg"},
		{"external-secrets", "externalsecrets-auto.svg"},
		{"tg", "terragrunt-auto.svg"},
		{"tofu", "opentofu-auto.svg"},
		{"open-tofu", "opentofu-auto.svg"},
		{"arm-assembly", "arm-auto.svg"},
		{"httpd", "apache-auto.svg"},
		{"grafana-alloy", "alloy-auto.svg"},
		{"claude-code", "claudecode-auto.svg"},
		{"codex-cli", "codex-auto.svg"},
		{"antigravity-cli", "antigravity-auto.svg"},
		{"oss-fuzz", "ossfuzz-auto.svg"},
		{"tektoncd", "tekton-auto.svg"},
	} {
		t.Run("alias/"+alias.input, func(t *testing.T) {
			assertIconResponse(t, alias.input, "", alias.target)
		})
	}
}

func TestWebStackIcons(t *testing.T) {
	for _, name := range []string{
		"html", "css", "bootstrap",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}
}

func TestNewIcons2(t *testing.T) {
	for _, name := range []string{
		"kargo", "kubescape", "opa", "kyverno", "backstage",
		"trivy", "talos", "cilium", "haproxy", "nix", "uv",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}

	for _, alias := range []struct {
		input, target string
	}{
		{"open-policy-agent", "opa-auto.svg"},
		{"cplusplus", "cpp.svg"},
		{"csharp", "cs.svg"},
		{"taloslinux", "talos-auto.svg"},
	} {
		t.Run("alias/"+alias.input, func(t *testing.T) {
			assertIconResponse(t, alias.input, "", alias.target)
		})
	}
}

func TestExplicitThemesForIconsWithBaseAssets(t *testing.T) {
	// These icons have both a custom default and explicit theme variants.
	// An explicit theme must not silently return the auto-themed base file.
	for _, name := range []string{
		"ansible", "chainlink", "fastapi", "flask", "gitlab", "golang",
		"infura", "javascript", "mongodb", "nginx", "typescript",
		"cpp", "cs", "sentry", "c", "windows11", "mongoose",
	} {
		for _, theme := range []string{"dark", "light"} {
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+theme+".svg")
			})
		}
	}
}

func TestLatestRequestedIcons(t *testing.T) {
	for _, name := range []string{
		"c", "istio", "opencost", "mongoose", "flutter",
		"firebase", "sqlalchemy", "riverpod", "hyperledger",
		"kaleido", "windows11",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}

	for _, alias := range []struct {
		input, target string
	}{
		{"win11", "windows11-auto.svg"},
		{"hlf", "hyperledger-auto.svg"},
		{"hyperledgerfabric", "hyperledger-auto.svg"},
		{"hyperledger-fabric", "hyperledger-auto.svg"},
		{"cost", "opencost-auto.svg"},
		{"open-cost", "opencost-auto.svg"},
	} {
		t.Run("alias/"+alias.input, func(t *testing.T) {
			assertIconResponse(t, alias.input, "", alias.target)
		})
	}
}

func TestBatchNewIcons(t *testing.T) {
	for _, name := range []string{
		"sops", "buildpacks", "artifacthub", "cloudnativepg", "k9s", "k6",
		"kaniko", "nexus", "openfaas", "keda", "telepresence", "flagger",
		"knative", "coredns", "kubevip", "calico", "flannel", "cni",
		"containerd", "kubebench", "syft", "grype", "makefile", "taskfile",
		"hurl", "beats", "hubble", "tetragon", "robusta", "armo",
		"metamask", "rabby", "ranger", "cosign",
	} {
		for _, theme := range []string{"", "dark", "light"} {
			assetTheme := theme
			if assetTheme == "" {
				assetTheme = "auto"
			}
			t.Run(name+"/"+theme, func(t *testing.T) {
				assertIconResponse(t, name, theme, name+"-"+assetTheme+".svg")
			})
		}
	}

	for _, alias := range []struct {
		input, target string
	}{
		{"cnpg", "cloudnativepg-auto.svg"},
		{"kube-vip", "kubevip-auto.svg"},
		{"kube-bench", "kubebench-auto.svg"},
		{"make", "makefile-auto.svg"},
		{"task", "taskfile-auto.svg"},
		{"elasticbeats", "beats-auto.svg"},
		{"elastic-beats", "beats-auto.svg"},
		{"armo-platform", "armo-auto.svg"},
		{"armoplatform", "armo-auto.svg"},
		{"rabby-wallet", "rabby-auto.svg"},
		{"rabbywallet", "rabby-auto.svg"},
		{"container-d", "containerd-auto.svg"},
		{"open-faas", "openfaas-auto.svg"},
		{"tele-presence", "telepresence-auto.svg"},
		{"meta-mask", "metamask-auto.svg"},
		{"artifact-hub", "artifacthub-auto.svg"},
		{"apache-ranger", "ranger-auto.svg"},
		{"apacheranger", "ranger-auto.svg"},
		{"sigstore-cosign", "cosign-auto.svg"},
		{"sigstorecosign", "cosign-auto.svg"},
		{"eso", "externalsecrets-auto.svg"},
		{"otel", "opentelemetry-auto.svg"},
		{"opentel", "opentelemetry-auto.svg"},
		{"syth", "syft-auto.svg"},
	} {
		t.Run("alias/"+alias.input, func(t *testing.T) {
			assertIconResponse(t, alias.input, "", alias.target)
		})
	}
}

func TestProfileStrips(t *testing.T) {
	strips := []string{
		"aws,azure,gcp,digitalocean,terraform,terragrunt,opentofu,ansible,crossplane,backstage,packer,vagrant,vmware,vercel",
		"kubernetes,docker,helm,kustomize,argocd,flux,rke2,talos,kargo",
		"githubactions,gitlab,jenkins,circleci,tekton",
		"cilium,istio,linkerd,envoy,consul,nginx,apache,haproxy,keepalived",
		"prometheus,grafana,alloy,loki,tempo,mimir,pyroscope,jaeger,opentelemetry,elasticsearch,logstash,kibana,fluentd,dynatrace,sentry,opencost",
		"vault,certmanager,trivy,falco,externalsecrets,opa,kyverno,kubescape,sonarqube,ossfuzz",
		"harbor,redis,rabbitmq,longhorn",
		"postgres,mysql,mongodb,sqlserver,etcd,sqlalchemy,mongoose",
		"go,py,rust,bash,powershell,linux,ubuntu,debian,redhat,nixos,git,c,cpp,cs,windows11",
		"vscode,vim,zed,yaml,json,markdown,regex,latex",
		"claudecode,codex,antigravity,cursor,githubcopilot,ollama,mcp",
		"containerd,cni,calico,flannel,coredns,kubevip,hubble",
		"sops,kubebench,syft,grype,tetragon,armo",
		"kaniko,buildpacks,artifacthub,flagger,nexus,robusta",
		"keda,knative,openfaas,telepresence,k9s",
		"airflow,airbyte,trino,qdrant,cloudnativepg,rancher",
		"makefile,taskfile,hurl,k6,beats",
		"ts,js,html,css,bootstrap,nodejs,fastapi,flask,blazor,dotnet,flutter,riverpod,firebase,graphql",
		"solidity,vyper,ethereum,hyperledger,kaleido,hardhat,foundry,ipfs,chainlink,infura,alchemy,metamask,rabby",
		// New reorganized profile strips:
		"aws,azure,gcp,digitalocean,terraform,opentofu,terragrunt,ansible,packer,vmware,vagrant,crossplane,backstage",
		"docker,containerd,kubernetes,rke2,talos,helm,kustomize,keda",
		"githubactions,gitlab,jenkins,circleci,tekton,argocd,flux,kargo,flagger,harbor,nexus",
		"cilium,hubble,calico,coredns,istio,linkerd,envoy,consul,nginx,apache,haproxy,keepalived",
		"prometheus,grafana,alloy,mimir,loki,tempo,pyroscope,opentelemetry,jaeger,elasticsearch,logstash,kibana,fluentd,opencost",
		"vault,externalsecrets,sops,certmanager,opa,kyverno,ranger,trivy,kubescape,kubebench,syft,grype,falco,tetragon",
		"postgres,cloudnativepg,mysql,sqlserver,mongodb,redis,etcd,longhorn,rabbitmq",
		"go,py,rust,c,cpp,cs,bash,powershell,linux,ubuntu,debian,redhat,nixos,windows11",
		"git,vscode,vim,zed,makefile,taskfile,k9s,telepresence,hurl,k6,sqlalchemy,mongoose",
		"yaml,json,markdown,latex,regex",
		"cni,flannel,kubevip",
		"kaniko,buildpacks,artifacthub,knative,openfaas",
		"dynatrace,sentry,beats,robusta",
		"sonarqube,ossfuzz,armo",
		"airbyte,airflow,trino,qdrant",
		"html,css,bootstrap,js,ts,nodejs,fastapi,flask,dotnet,blazor,graphql,flutter,riverpod,firebase,vercel",
		"ethereum,hyperledger,kaleido,solidity,vyper,hardhat,foundry,chainlink,ipfs,infura,alchemy,metamask,rabby",
		// Ultimate categorization strips:
		"aws,azure,gcp,digitalocean,vmware,terraform,opentofu,terragrunt,crossplane,backstage,ansible,packer,vagrant",
		"kubernetes,rke2,talos,helm,kustomize,docker,containerd",
		"githubactions,gitlab,jenkins,circleci,tekton,argocd,flux,kargo,flagger,harbor,nexus,artifacthub",
		"istio,consul,linkerd,cilium,calico,flannel,envoy,coredns,cni,kubevip,nginx,apache,haproxy,keepalived",
		"prometheus,grafana,loki,mimir,tempo,pyroscope,alloy,dynatrace,sentry,robusta,opentelemetry,jaeger,elasticsearch,logstash,kibana,beats,fluentd",
		"kyverno,opa,ranger,certmanager,vault,sops,externalsecrets,tetragon,falco,armo,trivy,kubescape,kubebench,syft,grype,cosign",
	}

	for _, strip := range strips {
		for _, theme := range []string{"", "dark", "light"} {
			t.Run(strip+"/"+theme, func(t *testing.T) {
				query := url.Values{"i": {strip}, "theme": {theme}}
				recorder := httptest.NewRecorder()
				Handler(recorder, httptest.NewRequest(http.MethodGet, "/api/icons?"+query.Encode(), nil))
				if recorder.Code != http.StatusOK {
					t.Fatalf("status = %d, want %d", recorder.Code, http.StatusOK)
				}
				if got := recorder.Header().Get("Content-Type"); got != "image/svg+xml" {
					t.Errorf("Content-Type = %q, want image/svg+xml", got)
				}
				decoder := xml.NewDecoder(strings.NewReader(recorder.Body.String()))
				for {
					_, err := decoder.Token()
					if err == io.EOF {
						break
					}
					if err != nil {
						t.Fatalf("invalid SVG response for %s: %v", strip, err)
					}
				}
			})
		}
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
