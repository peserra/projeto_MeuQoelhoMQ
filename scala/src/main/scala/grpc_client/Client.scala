package grpc_client

import io.grpc.{ManagedChannel, ManagedChannelBuilder}
import teste_grpc.simple.{ChannelType, CreateChannelRequest, CreateChannelResponse, ListChannelsRequest, ListChannelsResponse, MessageManagerGrpc}
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
import teste_grpc.simple.MessageManagerGrpc.MessageManagerStub

object Client extends App {
    val channel1: ManagedChannel = ManagedChannelBuilder.forAddress("127.0.0.1", 12345).build()
    val stub: MessageManagerStub = MessageManagerGrpc.stub(channel1)

    val createChannelRequest: CreateChannelRequest = CreateChannelRequest("canal1", ChannelType.SIMPLE)

    val listChannelsRequest: ListChannelsRequest = ListChannelsRequest()

    val createChannelResponse: Future[CreateChannelResponse] = stub.createChannel(createChannelRequest)
    
    println("recebido do server " + createChannelResponse.toString)

    val listChannelsResponse: Future[ListChannelsResponse] = stub.listChannels(listChannelsRequest)
      
      listChannelsResponse.foreach(println)
    
  }
