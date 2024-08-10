import scalapb.compiler.Version.scalapbVersion
name := "grpc-client"
version := "0.1"

libraryDependencies ++= Seq(
  "io.grpc" % "grpc-netty" % "1.53.0",
  "io.grpc" % "grpc-protobuf" % "1.53.0",
  "io.grpc" % "grpc-stub" % "1.53.0",
  "com.thesamet.scalapb" %% "scalapb-runtime-grpc" % "0.11.11",
  "net.java.dev.jna" % "jna" % "5.9.0"
)

ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"
javaOptions += "-Djna.library.path=/path/to/jna"

lazy val root = (project in file("."))
  .settings(
    name := "grpc-scala-client",
    libraryDependencies ++= Seq(
      "io.grpc" % "grpc-netty" % "1.53.0",
      "io.grpc" % "grpc-protobuf" % "1.53.0",
      "io.grpc" % "grpc-stub" % "1.53.0",
      "com.thesamet.scalapb" %% "scalapb-runtime-grpc" % "0.11.11"
    ),
    Compile / PB.protoSources := Seq(file("../protos")),
    Compile / PB.targets := Seq(
      scalapb.gen(grpc = true) -> (Compile / sourceManaged).value / "scalapb"
    )
  )

Compile / PB.protoSources := Seq(file("../protos"))
Compile / PB.targets := Seq(
  scalapb.gen(grpc = true) -> (Compile / sourceManaged).value / "scalapb"
)
