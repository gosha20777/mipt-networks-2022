FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY . .
RUN dotnet publish "Server/MessengerWeb.Server.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:5.0 AS runtime
WORKDIR /opt/app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MessengerWeb.Server.dll"]