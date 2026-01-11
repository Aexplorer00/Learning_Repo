# Maven Quick Reference for SRE Interviews
## 10-Minute Crash Course

---

## 🎯 What is Maven?

**Maven** = Build automation tool for Java projects (like `pip` + `make` combined)

**Purpose:**
- Compile Java code
- Manage dependencies (libraries)
- Run tests
- Package applications (JAR/WAR files)
- Deploy artifacts

---

## 📦 Core Concepts

### 1. POM (Project Object Model) - `pom.xml`

The heart of every Maven project. Defines:
- Project metadata (name, version)
- Dependencies (external libraries)
- Build plugins
- Build configuration

**Example `pom.xml`:**
```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    
    <!-- Project Info -->
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <!-- Dependencies -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.7.0</version>
        </dependency>
    </dependencies>
</project>
```

**Key Elements:**
- `groupId`: Organization/company (like `com.google`)
- `artifactId`: Project name (like `my-service`)
- `version`: Project version (like `1.0.0`)
- `dependencies`: External libraries needed

---

### 2. Maven Build Lifecycle

**The Standard Phases (in order):**

| Phase | What It Does | Command |
|-------|--------------|---------|
| `validate` | Check project is correct | `mvn validate` |
| `compile` | Compile source code | `mvn compile` |
| `test` | Run unit tests | `mvn test` |
| `package` | Create JAR/WAR file | `mvn package` |
| `verify` | Run integration tests | `mvn verify` |
| `install` | Install to local repo | `mvn install` |
| `deploy` | Deploy to remote repo | `mvn deploy` |

**Important:** Running a phase executes ALL previous phases!

```bash
mvn package
# Runs: validate → compile → test → package
```

---

### 3. Common Maven Commands

```bash
# Clean build artifacts
mvn clean

# Compile + Test + Package (most common)
mvn clean package

# Skip tests (faster builds)
mvn clean package -DskipTests

# Run specific test
mvn test -Dtest=MyTest

# Install dependencies
mvn dependency:resolve

# Show dependency tree
mvn dependency:tree

# Run the application
mvn spring-boot:run  # For Spring Boot apps
```

---

## 🗂️ Maven Project Structure

```
my-app/
├── pom.xml                    ← Build configuration
├── src/
│   ├── main/
│   │   ├── java/              ← Application code
│   │   │   └── com/example/
│   │   │       └── App.java
│   │   └── resources/         ← Config files
│   │       └── application.properties
│   └── test/
│       ├── java/              ← Test code
│       │   └── com/example/
│       │       └── AppTest.java
│       └── resources/
└── target/                    ← Build output (JAR/WAR)
    └── my-app-1.0.0.jar
```

**Convention over Configuration:** Maven expects this structure!

---

## 🔧 Dependencies Management

### How Dependencies Work:

```xml
<dependencies>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>  <!-- Only for testing -->
    </dependency>
</dependencies>
```

**Dependency Scopes:**
- `compile`: Default, available everywhere
- `test`: Only for tests
- `provided`: Provided by runtime (e.g., servlet API)
- `runtime`: Not needed for compilation, only runtime

**Maven Central Repository:** Where Maven downloads dependencies from
- URL: https://repo.maven.apache.org/maven2/
- Like PyPI for Python, npm for Node.js

---

## 🎯 SRE Interview Questions & Answers

### Q1: What's the difference between Maven and Gradle?
> **Maven:** XML-based, convention over configuration, simpler but verbose.  
> **Gradle:** Groovy/Kotlin-based, more flexible, faster builds, used by Android.

### Q2: What's a Maven artifact?
> A packaged output (JAR, WAR, or EAR file) that can be deployed or reused.

### Q3: How do you troubleshoot a Maven build failure?
> 1. Check `mvn -X` (debug mode) for detailed logs
> 2. Run `mvn clean` to remove stale artifacts
> 3. Check `pom.xml` for dependency conflicts
> 4. Verify Java version compatibility

### Q4: What's a Maven repository?
> - **Local:** `~/.m2/repository` (cached dependencies on your machine)
> - **Remote:** Maven Central or company Nexus/Artifactory

### Q5: How do you skip tests in CI/CD?
> `mvn clean package -DskipTests` (compiles tests but doesn't run them)  
> `mvn clean package -Dmaven.test.skip=true` (skips compilation too)

---

## 🐳 Maven in Docker (Common SRE Scenario)

**Multi-stage Dockerfile for Java app:**

```dockerfile
# Stage 1: Build with Maven
FROM maven:3.8-openjdk-11 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline  # Cache dependencies
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM openjdk:11-jre-slim
COPY --from=build /app/target/my-app.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

**Why multi-stage?**
- Build image has Maven (large)
- Runtime image only has Java (small)
- Final image is ~200MB instead of ~800MB

---

## 🔄 Maven in CI/CD Pipeline

**GitHub Actions Example:**

```yaml
name: Java CI

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up JDK 11
        uses: actions/setup-java@v2
        with:
          java-version: '11'
      
      - name: Build with Maven
        run: mvn clean package
      
      - name: Run tests
        run: mvn test
      
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: my-app.jar
          path: target/*.jar
```

---

## 📊 Maven vs Other Build Tools

| Tool | Language | Config File | Speed | Flexibility |
|------|----------|-------------|-------|-------------|
| **Maven** | Java | `pom.xml` (XML) | Medium | Low |
| **Gradle** | Java/Kotlin/Groovy | `build.gradle` | Fast | High |
| **Ant** | Java | `build.xml` | Slow | High |
| **pip** | Python | `requirements.txt` | Fast | N/A |
| **npm** | JavaScript | `package.json` | Fast | Medium |

---

## 🚨 Common Issues & Fixes

### Issue 1: "Failed to execute goal"
```bash
# Solution: Clean and rebuild
mvn clean install
```

### Issue 2: "Dependency not found"
```bash
# Solution: Update Maven repo
mvn dependency:purge-local-repository
```

### Issue 3: "OutOfMemoryError"
```bash
# Solution: Increase Maven memory
export MAVEN_OPTS="-Xmx1024m"
mvn clean package
```

---

## 🎓 Key Takeaways for SRE

1. **Maven = Build + Dependency Management** for Java
2. **`pom.xml`** = Central configuration (like `package.json`)
3. **Lifecycle:** validate → compile → test → package → deploy
4. **Common command:** `mvn clean package -DskipTests`
5. **In Docker:** Use multi-stage builds to reduce image size
6. **In CI/CD:** Cache dependencies for faster builds

---

## 🔗 Quick Reference Commands

```bash
# Build project
mvn clean package

# Run tests
mvn test

# Skip tests
mvn package -DskipTests

# Show dependencies
mvn dependency:tree

# Update dependencies
mvn versions:display-dependency-updates

# Run Spring Boot app
mvn spring-boot:run
```

---

**That's it!** You now know enough Maven to ace SRE interviews. 🎯

*Created for: DEVOPS/SRE 60-Day Journey (Day 4)*
