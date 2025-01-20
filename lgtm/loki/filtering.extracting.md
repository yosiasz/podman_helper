## json

| json
| line_format "{{ .asctime }} | {{ .levelname }} | {{ .method }} | {{ .message }}"

## log

{filename="/tmp/jazz.log"} | pattern \`\<message\> <\_> \<timer\>\`

## regex

{filename="/tmp/jazz.log"} | regexp \`(?P<message>\w+) (?P<label>\w+:) (?P<elaspsed>\d+) \`
