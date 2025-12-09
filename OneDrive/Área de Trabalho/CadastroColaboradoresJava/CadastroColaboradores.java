import java.util.Scanner;

public class CadastroColaboradores {

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        Pessoa[] pessoas = new Pessoa[3];

        for (int i = 0; i < pessoas.length; i++) {
            System.out.print("Digite o nome da pessoa " + (i + 1) + ": ");
            String nome = entrada.nextLine();

            int idade = 0;
            boolean idadeValida = false;
            while (!idadeValida) {
                System.out.print("Digite a idade de " + nome + ": ");
                String idadeStr = entrada.nextLine();
                try {
                    idade = Integer.parseInt(idadeStr);
                    idadeValida = true;
                } catch (NumberFormatException e) {
                    System.out.println("❌ Erro: Digite apenas números para a idade.");
                }
            }

            pessoas[i] = new Pessoa(nome, idade);
        }

        mostrarResumo(pessoas);
        entrada.close();
    }

    static void mostrarResumo(Pessoa[] pessoas) {
        int soma = 0;
        Pessoa maisNovo = pessoas[0];
        Pessoa maisVelho = pessoas[0];

        for (Pessoa p : pessoas) {
            soma += p.idade;

            if (p.idade < maisNovo.idade) {
                maisNovo = p;
            }

            if (p.idade > maisVelho.idade) {
                maisVelho = p;
            }
        }

        double media = (double) soma / pessoas.length;

        System.out.println("\n📊 RESUMO:");
        System.out.println("Pessoa mais nova: " + maisNovo.nome + " (" + maisNovo.idade + " anos)");
        System.out.println("Pessoa mais velha: " + maisVelho.nome + " (" + maisVelho.idade + " anos)");
        System.out.println("Média das idades: " + media);
    }
}

class Pessoa {
    String nome;
    int idade;

    Pessoa(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }
}