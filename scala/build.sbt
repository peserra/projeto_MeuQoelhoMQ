val scala3Version = "3.3.0"
val http4sVersion = "0.23.23"
val weaverVersion = "0.8.3"
val squantsVersion = "1.8.3"

lazy val protobuf =
  project
    .in(file("protobuf"))
    .settings(
      name := "protobuf",
      scalaVersion := scala3Version,
      libraryDependencies += "com.thesamet.scalapb" %% "scalapb-runtime" % scalapb.compiler.Version.scalapbVersion % "protobuf",
      libraryDependencies += "org.typelevel" %% "squants" % squantsVersion
    )
    .enablePlugins(Fs2Grpc)

lazy val root =
  project
    .in(file("."))
    .settings(
      name := "root",
      scalaVersion := scala3Version,
      libraryDependencies ++= Seq(
        "io.grpc" % "grpc-netty-shaded" % scalapb.compiler.Version.grpcJavaVersion,
        "com.thesamet.scalapb" %% "scalapb-runtime" % scalapb.compiler.Version.scalapbVersion % "protobuf",
        "org.typelevel" %% "squants" % squantsVersion
      )
    )
    .dependsOn(protobuf)
