package grpc_client

import io.grpc.{ManagedChannel, ManagedChannelBuilder}
import teste_grpc.simple.{ChannelType, CreateChannelRequest, CreateChannelResponse, ListChannelsRequest, MessageManagerGrpc}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import teste_grpc.simple.MessageManagerGrpc.MessageManagerStub

object Client extends App {
    val channel: ManagedChannel = ManagedChannelBuilder.forAddress("localhost", 12345).build()
    val stub: MessageManagerStub = MessageManagerGrpc.stub(channel)

    val createChannelRequest: CreateChannelRequest = CreateChannelRequest("canal1", ChannelType.SIMPLE)
    val listChannelsRequest: ListChannelsRequest = ListChannelsRequest()
    val createChannelResponse: Future[CreateChannelResponse] = stub.createChannel(createChannelRequest)
    println(s"channel created: ${createChannelResponse.toString}")

    stub.listChannels(listChannelsRequest).foreach(println)
  }
