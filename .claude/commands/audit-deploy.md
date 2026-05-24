---
description: Pre-flight gate for Wless local maven deploys. Verifies JDK/Maven versions, pom.xml validity, dependency resolution, port availability, deploy.sh sanity. Emits 🟢/🟡/🔴 verdict.
---

# /audit-deploy <variant-or-module> [--port P]

Invokes `local-deploy-expert` + `maven-serverless-expert`.

## Scope

- `<variant>` like `Acmeair_0` → audits all `*Entry` modules
- `<variant>/<module>` like `Acmeair_0/MSauthEntry` → just that module

## Phases (5)

### 1. Toolchain
- `java -version 2>&1 | head -1` → must be `17` or higher
- `mvn -v | head -1` → must be `3.9+`
- 🔴 if either missing or too old

### 2. pom.xml validity
- `mvn -pl <module> -am validate -q`
- 🔴 if validation fails

### 3. Dependency resolution
- `mvn -pl <module> -am dependency:resolve -q --offline 2>&1 | tail`
- If offline fails: `mvn -pl <module> -am dependency:resolve -q`
- 🟡 if SNAPSHOT dependencies present (non-reproducible)
- 🔴 if resolution fails

### 4. Port availability
- Default port from `application.properties` (or `--port`)
- `lsof -iTCP:$port -sTCP:LISTEN -P -n` → must be empty
- 🟡 if occupied — suggest alternative free port

### 5. deploy.sh sanity (legacy)
- If `deploy.sh` exists: parse for `gcloud` invocations → 🔴 (boundary violation, must be migrated to local)
- 🟢 if no gcloud or if `deploy.sh` is the LOCAL variant

## Output

```markdown
# /audit-deploy report — Acmeair_0/MSauthEntry

## Toolchain: 🟢
- JDK 17.0.9
- Maven 3.9.6

## pom.xml: 🟢
## Dependencies: 🟡 (2 SNAPSHOT)
- `io.quarkus:quarkus-rest:999-SNAPSHOT` — pin to release version
## Port 8080: 🟢 free
## deploy.sh: 🔴 contains `gcloud run deploy` (line 14)
- ACTION: migrate to `java -jar target/*.jar --quarkus.http.port=8080`

## Overall: 🔴 (deploy.sh boundary violation)
```

## When to invoke

- Before `/wless-bench`
- As part of `/iterate` Phase 1 when pom or *Entry/ touched
- Standalone when troubleshooting deploy failures

## Constraints

- NEVER auto-fix `deploy.sh` (let user / specialist decide)
- ALWAYS check JDK + Maven first (fast)
- 🔴 on `gcloud`/`aws`/`az` references in deploy scripts
