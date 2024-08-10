package grpc

import io.grpc.ManagedChannelBuilder
import teste_grpc.simple.{ChannelType, CreateChannelRequest, ListChannelsRequest, MessageManagerGrpc}
import scala.concurrent.ExecutionContext.Implicits.global

object Client extends App {
    val channel = ManagedChannelBuilder.forAddress("localhost", 12345).build()
    val stub = MessageManagerGrpc.stub(channel)

    val createChannelRequest: CreateChannelRequest = CreateChannelRequest("canal1", ChannelType.SIMPLE)
    val listChannelsRequest: ListChannelsRequest = ListChannelsRequest()
    stub.createChannel(createChannelRequest)

    stub.listChannels(listChannelsRequest).foreach(println)
  }
