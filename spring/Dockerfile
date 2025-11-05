# Build stage
FROM gradle:8.10.2-jdk17 AS builder
WORKDIR /workspace
COPY build.gradle settings.gradle gradlew ./
COPY gradle ./gradle
COPY src ./src
RUN ./gradlew clean bootJar --no-daemon

# Run stage
FROM eclipse-temurin:17-jre
ENV TZ=Asia/Seoul
WORKDIR /app

# curl 설치 (이미지 용량 최소화)
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /workspace/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
