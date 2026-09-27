import json
import re

with open('api/index.go') as f:
    for line in f:
        line_s = line.strip()
        if line_s.startswith('var iconsJSON = `'):
            raw = line_s[len('var iconsJSON = `'):-1]
            icons = json.loads(raw)
            break

shortNames = {
	"js":                "javascript",
	"ts":                "typescript",
	"py":                "python",
	"tailwind":          "tailwindcss",
	"vue":               "vuejs",
	"nuxt":              "nuxtjs",
	"go":                "golang",
	"cert-manager":      "certmanager",
	"external-secrets":  "externalsecrets",
	"tg":                "terragrunt",
	"cf":                "cloudflare",
	"wasm":              "webassembly",
	"postgres":          "postgresql",
	"k8s":               "kubernetes",
	"next":              "nextjs",
	"mongo":             "mongodb",
	"md":                "markdown",
	"ps":                "photoshop",
	"ai":                "illustrator",
	"pr":                "premiere",
	"ae":                "aftereffects",
	"scss":              "sass",
	"sc":                "scala",
	"net":               "dotnet",
	"gatsbyjs":          "gatsby",
	"gql":               "graphql",
	"vlang":             "v",
	"amazonwebservices": "aws",
	"bots":              "discordbots",
	"express":           "expressjs",
	"googlecloud":       "gcp",
	"mui":               "materialui",
	"windi":             "windicss",
	"unreal":            "unrealengine",
	"nest":              "nestjs",
	"ktorio":            "ktor",
	"pwsh":              "powershell",
	"au":                "audition",
	"rollup":            "rollupjs",
	"rxjs":              "reactivex",
	"rxjava":            "reactivex",
	"ghactions":         "githubactions",
	"sklearn":           "scikitlearn",
	"ml5":               "ml5js",
	"vb":                "visualbasic",
	"an":                "animate",
	"ca":                "capture",
	"cc":                "creativecloud",
	"ch":                "characteranimator",
	"me":                "mediaencoder",
	"pl":                "prelude",
	"ru":                "premiererush",
	"fs":                "fuse",
	"id":                "indesign",
	"ic":                "incopy",
	"sp":                "adobespark",
	"dw":                "dreamweaver",
	"dn":                "dimension",
	"ar":                "aero",
	"psc":               "photoshopclassic",
	"psx":               "photoshopexpress",
	"lr":                "lightroom",
	"lrc":               "lightroomclassic",
	"fr":                "fresco",
	"pf":                "portfolio",
	"st":                "stock",
	"be":                "behance",
	"br":                "bridge",
	"million":           "millionjs",
	"asm":               "assembly",
	"pop":               "popos",
	"nix":               "nixos",
	"hc":                "holyc",
	"yml":               "yaml",
	"twitter":           "x",
	"arc":               "arcbrowser",
	"hf":                "huggingface",
	"sqla":              "sqlalchemy",
    "notepad++":         "notepadpp",
    "jq":                "jqlang",
}

iconNameList = []
themedIcons = []
for k in icons:
    base = k.split('-')[0]
    iconNameList.append(base)
    if any(k.endswith(s) for s in ['-auto', '-dark', '-light']):
        themedIcons.append(base)

def resolve_icons(names, theme):
    res = []
    for name in names:
        if name in icons:
            res.append(name)
            continue
        if name in iconNameList:
            if name in themedIcons:
                res.append(name + '-' + theme)
            else:
                res.append(name)
        elif name in shortNames:
            val = shortNames[name]
            if val in themedIcons:
                res.append(val + '-' + theme)
            else:
                res.append(val)
        else:
            res.append(name)
    return res

urls = [
    'aws,azure,gcp,digitalocean,terraform,terragrunt,crossplane,ansible,packer,vagrant,vmware',
    'kubernetes,rke2,docker,helm,kustomize,argocd,flux,rancher',
    'githubactions,gitlab,jenkins,circleci',
    'cilium,istio,linkerd,kuma,consul,nginx,cloudflare',
    'prometheus,grafana,loki,tempo,jaeger,opentelemetry,elasticsearch,logstash,kibana,fluentd',
    'vault,externalsecrets,falco,trivy,certmanager,sonarqube',
    'minio,longhorn,harbor,kafka,rabbitmq,redis',
    'postgres,mysql,mongodb,etcd,sqlserver',
    'go,py,bash,linux,ubuntu,debian,redhat,c,rust,git',
    'vim,vscode,tmux,postman,ollama',
    'ts,js,nodejs,fastapi,flask,dotnet,graphql,tailwind,react,nextjs',
    'solidity,ethereum,hardhat,foundry,ipfs,chainlink'
]

print("=== CHECKING ID COLLISIONS PER URL STRIP ===")
for url in urls:
    names = url.split(',')
    resolved = resolve_icons(names, 'auto')
    all_ids = {}
    for raw, res in zip(names, resolved):
        content = icons.get(res, '')
        ids = re.findall(r'\bid=[\"\']([^\"\']+)[\"\']', content)
        for i in ids:
            if i in all_ids:
                all_ids[i].append((raw, res))
            else:
                all_ids[i] = [(raw, res)]
    
    collisions = {k: v for k, v in all_ids.items() if len(v) > 1}
    if collisions:
        print(f"\nURL: {url}")
        for k, v in collisions.items():
            print(f'  ID collision on id="{k}": {[r[0] for r in v]}')
