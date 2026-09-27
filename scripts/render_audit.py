import os, subprocess, json
from PIL import Image

with open('api/index.go') as f:
    for line in f:
        line_s = line.strip()
        if line_s.startswith('var iconsJSON = '):
            idx = line_s.find('`')
            raw = line_s[idx+1:-1]
            icons = json.loads(raw)
            break

shortNames = {
	'js': 'javascript', 'ts': 'typescript', 'py': 'python', 'tailwind': 'tailwindcss',
	'vue': 'vuejs', 'nuxt': 'nuxtjs', 'go': 'golang', 'cert-manager': 'certmanager',
	'external-secrets': 'externalsecrets', 'tg': 'terragrunt', 'cf': 'cloudflare',
	'wasm': 'webassembly', 'postgres': 'postgresql', 'k8s': 'kubernetes', 'next': 'nextjs',
	'mongo': 'mongodb', 'md': 'markdown', 'ps': 'photoshop', 'ai': 'illustrator',
	'pr': 'premiere', 'ae': 'aftereffects', 'scss': 'sass', 'sc': 'scala',
	'net': 'dotnet', 'gatsbyjs': 'gatsby', 'gql': 'graphql', 'vlang': 'v',
	'amazonwebservices': 'aws', 'bots': 'discordbots', 'express': 'expressjs',
	'googlecloud': 'gcp', 'mui': 'materialui', 'windi': 'windicss', 'unreal': 'unrealengine',
	'nest': 'nestjs', 'ktorio': 'ktor', 'pwsh': 'powershell', 'au': 'audition',
	'rollup': 'rollupjs', 'rxjs': 'reactivex', 'rxjava': 'reactivex', 'ghactions': 'githubactions',
	'sklearn': 'scikitlearn', 'ml5': 'ml5js', 'vb': 'visualbasic', 'an': 'animate',
	'ca': 'capture', 'cc': 'creativecloud', 'ch': 'characteranimator', 'me': 'mediaencoder',
	'pl': 'prelude', 'ru': 'premiererush', 'fs': 'fuse', 'id': 'indesign',
	'ic': 'incopy', 'sp': 'adobespark', 'dw': 'dreamweaver', 'dn': 'dimension',
	'ar': 'aero', 'psc': 'photoshopclassic', 'psx': 'photoshopexpress', 'lr': 'lightroom',
	'lrc': 'lightroomclassic', 'fr': 'fresco', 'pf': 'portfolio', 'st': 'stock',
	'be': 'behance', 'br': 'bridge', 'million': 'millionjs', 'asm': 'assembly',
	'pop': 'popos', 'nix': 'nixos', 'hc': 'holyc', 'yml': 'yaml',
	'twitter': 'x', 'arc': 'arcbrowser', 'hf': 'huggingface', 'sqla': 'sqlalchemy',
    'notepad++': 'notepadpp', 'jq': 'jqlang'
}

iconNameList = []
themedIcons = []
for k in icons:
    base = k.split('-')[0]
    iconNameList.append(base)
    if any(k.endswith(s) for s in ['-auto', '-dark', '-light']):
        themedIcons.append(base)

def resolve_icon(name, theme):
    if name in icons:
        return name
    if name in iconNameList:
        return (name + '-' + theme) if name in themedIcons else name
    if name in shortNames:
        val = shortNames[name]
        return (val + '-' + theme) if val in themedIcons else val
    return name

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

checked = set()
for url in urls:
    for ic in url.split(','):
        checked.add(ic)

print(f'Checking {len(checked)} unique icons across dark and light...')

os.makedirs('/tmp/svg_check', exist_ok=True)

for ic in sorted(checked):
    for theme in ['dark', 'light']:
        resolved = resolve_icon(ic, theme)
        svg_data = icons.get(resolved, '')
        if not svg_data:
            print(f'MISSING ICON: {ic} (theme={theme}, resolved={resolved})')
            continue
        svg_file = f'/tmp/svg_check/{resolved}.svg'
        png_file = f'/tmp/svg_check/{resolved}.png'
        with open(svg_file, 'w') as f:
            f.write(svg_data)
        ret = subprocess.run(['convert', svg_file, png_file], capture_output=True)
        if ret.returncode != 0:
            print(f'CONVERT ERROR on {resolved}: {ret.stderr.decode()[:100]}')
            continue
        im = Image.open(png_file)
        w, h = im.size
        center_crop = im.crop((int(w*0.25), int(h*0.25), int(w*0.75), int(h*0.75)))
        crop_colors = center_crop.getcolors(maxcolors=1000)
        num_crop_colors = len(crop_colors) if crop_colors else 1000
        if num_crop_colors <= 2:
            print(f'BLANK / JUST BACKGROUND: {ic} (resolved={resolved}, theme={theme}, crop_colors={num_crop_colors})')
print('Done!')
