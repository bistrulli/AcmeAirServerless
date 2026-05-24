---
name: maven-serverless-patterns
description: Wless Maven + serverless function patterns - pom.xml archetypes (Quarkus, Spring Cloud Function, Micronaut), local run commands, JUnit 5 + AssertJ, concurrency knobs, native-image profile. Use when editing pom.xml or src/main/java in Acmeair_variants/*/Entry/.
---

# Maven serverless patterns (Wless)

## Framework choice

| Framework | Strengths | Choose when |
|---|---|---|
| **Quarkus** ⭐ | ~50 ms startup, GraalVM native, dev-mode hot reload | DEFAULT for Wless |
| **Spring Cloud Function** | Spring ecosystem, FaaS-portable | Existing Spring code |
| **Micronaut** | AOT, reflection-free, fast startup | Fits AWS Lambda style |

Default for Wless: **Quarkus** (fast startup → reliable Locust experiments).

## Quarkus pom.xml archetype

See `agents/maven-serverless-expert.md` for full pom. Key sections:

```xml
<properties>
  <maven.compiler.release>17</maven.compiler.release>
  <quarkus.version>3.10.0</quarkus.version>          <!-- PIN, no LATEST -->
</properties>
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>io.quarkus.platform</groupId>
      <artifactId>quarkus-bom</artifactId>
      <version>${quarkus.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

## Local run commands

```bash
# Dev mode (hot reload)
mvn quarkus:dev

# Production-style jar
mvn -DskipTests=false package
java -jar target/quarkus-app/quarkus-run.jar --quarkus.http.port=8080

# Native build (Wless rarely needs this — JVM is fine for benchmarks)
mvn -Pnative package
./target/<name>-runner --quarkus.http.port=8080
```

## JUnit 5 + AssertJ patterns

```java
@QuarkusTest
class AuthResourceTest {
    @Test
    void authReturnsOk() {
        given().when().get("/auth")
               .then().statusCode(200).body("status", is("ok"));
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 10, 100})
    void handlesMultipleSizes(int n) {
        var result = service.process(n);
        assertThat(result).hasSize(n).allMatch(Objects::nonNull);
    }
}
```

## Concurrency knobs

Map Wless scenarios to Quarkus config:

| Scenario | Property | Value |
|---|---|---|
| `defconc` | `quarkus.thread-pool.max-threads` | 80 |
| `noconc` | `quarkus.thread-pool.max-threads` | 1 |
| `noconc` | `quarkus.thread-pool.core-threads` | 1 |
| `wlessconc` | `quarkus.thread-pool.max-threads` | from `optSol.csv` |
| `propackconc` | `quarkus.thread-pool.max-threads` | from `ProPackSol.csv` |

Place per-scenario `application.properties` in `src/main/resources/scenarios/<name>.properties`. Select at runtime:

```bash
java -jar target/quarkus-app/quarkus-run.jar \
     -Dquarkus.config.locations=src/main/resources/scenarios/wlessconc.properties
```

## Common pitfalls (and fixes)

| Symptom | Cause | Fix |
|---|---|---|
| `Address already in use: 8080` | Previous run not torn down | `lsof -ti :8080 \| xargs kill -9` |
| `@QuarkusTest` not found | Missing `quarkus-junit5` test dep | Add with `scope=test` |
| Slow first start (>10s) | Large dep graph, JIT | Trim deps or native build |
| Native build OOM | GraalVM heap default low | `-J-Xmx4g` in plugin config |
| `Connection refused` from Locust | Readiness probe not waited | Poll `/q/health` before workload |

## Dependency hygiene

- PIN all versions (no `LATEST`, no unresolved `RELEASE`)
- One `quarkus-bom` import per module
- No `spring-*` deps when on Quarkus (and vice versa)
- No `com.google.cloud:*` deps (Wless is moving AWAY from GCR)
- Test scope: AssertJ, JUnit 5, REST-assured
- Production scope: SLF4J via `org.jboss.logging.Logger` (Quarkus default)

## Constraints

- NEVER `System.out.println` in production code — use logger
- NEVER mix Spring + Quarkus in the same pom
- ALWAYS pin Quarkus + AssertJ + Surefire versions
- ALWAYS include `--quarkus.http.port=<P>` at run-time (don't hard-code 8080)
