package grpc_client

import io.grpc.{ManagedChannel, ManagedChannelBuilder}
import teste_grpc.simple.{ChannelType, CreateChannelRequest, ListChannelsRequest, MessageManagerGrpc}
import scala.concurrent.ExecutionContext.Implicits.global
import teste_grpc.simple.MessageManagerGrpc.MessageManagerStub

object Client extends App {
    val channel: ManagedChannel = ManagedChannelBuilder.forAddress("localhost", 12345).build()
    val stub: MessageManagerStub = MessageManagerGrpc.stub(channel)

    val createChannelRequest: CreateChannelRequest = CreateChannelRequest("canal1", ChannelType.SIMPLE)
    val listChannelsRequest: ListChannelsRequest = ListChannelsRequest()
    stub.createChannel(createChannelRequest)

    stub.listChannels(listChannelsRequest).foreach(println)
  }
